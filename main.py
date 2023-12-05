import os

from langchain.chains import LLMMathChain
from langchain.llms import OpenAI
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.tools.ddg_search import DuckDuckGoSearchRun
from langchain.tools.human import HumanInputRun
from langchain.utilities import SerpAPIWrapper, SQLDatabase
from langchain.agents import Tool, AgentType, initialize_agent, load_tools
from langchain.agents.openai_functions_multi_agent.base import OpenAIMultiFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from Prompts.SystemPrompt import (super_prompt, default_context, conversation_prompt)
import asyncio

os.environ["OPENAI_API_KEY"] = ''
os.environ["SERPER_API_KEY"] = '29ce322a9d04ab78fc16d78f2caea4a40664670d'

SUFFIX = """
Here they are:
{chat_history}
Question: {input}
{agent_scratchpad}
"""

def get_input() -> str:
    print("Insert your text. Enter 'q' or press Ctrl-D (or Ctrl-Z on Windows) to end.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "q":
            break
        contents.append(line)
    return "\n".join(contents)

async def newAgent():
    llm = ChatOpenAI(temperature=0.5, model="gpt-4-1106-preview")

    # tools = [DuckDuckGoSearchRun(), HumanInputRun(input_func=get_input)]
    tools = load_tools(["google-serper", "dalle-image-generator"], llm=llm)

    # Create the memory
    memory = ConversationBufferMemory(memory_key="chat_history", input_key='input', output_key="output", return_messages=True)

    # Create the agent
    agent_kwargs = {
        # "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
        # 'prefix': conversation_prompt,
        "format_instructions": conversation_prompt,
        'suffix': SUFFIX
    }

    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs=agent_kwargs,
        memory=memory,
        return_intermediate_steps=True
    )

    response = await agent_chain.ainvoke(
        {"input": default_context}
    )
    print(response["output"])

    response = await agent_chain.ainvoke(
        {"input": "Generate list of most possible answers to your requirements (max 6 rows). Rely on input"}
    )
    print(response["output"])

    response = await agent_chain.ainvoke(
        {"input": "Generate logo image for this event"}
    )
    print(response["output"])

if __name__ == '__main__':
    asyncio.run(newAgent())