import os
from operator import itemgetter

from fastapi import FastAPI
from langchain.agents import initialize_agent, AgentType, AgentExecutor, ConversationalChatAgent, LLMSingleActionAgent, \
    AgentOutputParser
from langchain.agents.agent import RunnableMultiActionAgent
from langchain.agents.format_scratchpad import format_log_to_str, format_to_openai_function_messages
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.callbacks import FinalStreamingStdOutCallbackHandler
from langchain.chains import ConversationChain, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.tools.render import render_text_description, format_tool_to_openai_function
from langchain.utilities.dalle_image_generator import DallEAPIWrapper
from langchain.utilities.google_serper import GoogleSerperAPIWrapper
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate, BaseChatPromptTemplate
from langchain_core.runnables import ConfigurableField, RunnablePassthrough, RunnableLambda
from langchain_core.tools import Tool
from langserve import add_routes, CustomUserType
import uvicorn
from pydantic import BaseModel

from Prompts.SystemPrompt import chat_prompt, super_prompt, generation_prompt, examples


class Input(BaseModel):
    input: str | None


class Output(BaseModel):
    output: str | None


app = FastAPI(
    title='Project',
)

os.environ["OPENAI_API_KEY"] = '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'
os.environ["SERPER_API_KEY"] = '29ce322a9d04ab78fc16d78f2caea4a40664670d'

llm = ChatOpenAI(temperature=0.0,
                 model="gpt-4-1106-preview",
                 streaming=True,
                 callbacks=[FinalStreamingStdOutCallbackHandler()]).configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",
        name="LLM Temperature",
        description="The temperature of the LLM"))

search = GoogleSerperAPIWrapper()

tools = [
    Tool(
        name="search",
        func=search.run,
        description=""""A search engine optimized for comprehensive, accurate, \
            and trusted results. Useful for when you need to answer questions \
            about current events or about recent information. \
            Input should be a search query. \
            If the user is asking about something that you don't know about, \
            you should probably use this tool to see if that can provide any information.""",
    )]

prompt = PromptTemplate.from_template(generation_prompt)

prompt = prompt.partial(
    tools=render_text_description(tools),
    tool_names=", ".join([t.name for t in tools]),
    examples=examples
)

llm_with_stop = llm.bind(stop=["\nObservation"])

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"]),
    }
        | prompt
        | llm_with_stop
        | ReActSingleInputOutputParser()
)

agent_executor = AgentExecutor(agent=agent,
                               tools=tools,
                               verbose=True,
                               handle_parsing_errors=True)


agent_executor = agent_executor.with_types(input_type=Input, output_type=Output)

add_routes(
    app,
    agent_executor,
    path="/generator",
)

if __name__ == '__main__':
    uvicorn.run('plan_generator:app')
