import os
import asyncio
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.agents import Tool, initialize_agent, AgentType, load_tools, AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.tools import DuckDuckGoSearchRun, E2BDataAnalysisTool, HumanInputRun
from langchain.utilities.google_serper import GoogleSerperAPIWrapper
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder

from Models.Model import event, contacts
from Prompts.SystemPrompt import (super_prompt, default_context, conversation_prompt)
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory

os.environ["OPENAI_API_KEY"] = ''
os.environ["SERPER_API_KEY"] = '29ce322a9d04ab78fc16d78f2caea4a40664670d'
# os.environ["E2B_API_KEY"] = 'e2b_e13d23d507cf8b524363d563a0eec57be35019ff'
search = GoogleSerperAPIWrapper()
# DuckDuckGoSearchRun(),
# tools = [Tool(name="Intermediate Answer", func=search.run, description="use for search in internet",)]
# memory = ConversationBufferMemory(memory_key="chat_history", input_key='input', output_key="output")


agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
}
memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

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
    # agent_kwargs = {
    #     'format_instructions': conversation_prompt
    # }

    # llm = ChatOpenAI(temperature=0.3, model_name="gpt-4-1106-preview")
    tools = [
        # DuckDuckGoSearchRun(),
        HumanInputRun(input_func=get_input),
        # {"type": "code_interpreter"}
             ]
    # tools = load_tools(["google-serper"], llm=llm)

    # agent_chain = initialize_agent(
    #     tools,
    #     llm,
    #     agent=AgentType.OPENAI_FUNCTIONS,
    #     verbose=True,
    #     agent_kwargs=agent_kwargs,
    #     memory=memory,
    #     return_intermediate_steps=True
    # )

    agent_chain = OpenAIAssistantRunnable.create_assistant(
        name="Event conversation tool",
        instructions=conversation_prompt,
        tools=tools,
        model="gpt-4-1106-preview",
        as_agent=True,
        memory=memory
    )

    agent_executor = AgentExecutor(agent=agent_chain, tools=tools)

    assistant_response = await agent_executor.ainvoke({
        "content": default_context,
    })
    print(assistant_response["output"])

    # response = await agent_chain.ainvoke(
    #     {"input": default_context}
    # )
    # print(response["output"])

    # response = await agent_chain.ainvoke(
    #     {"content": default_context}
    # )
    # print(response.return_values["output"])
    #
    # response = await agent_chain.ainvoke(
    #     {"content": "Generate list of most possible answers to your requirements (max 6 rows). Rely on input"}
    # )
    # print(response.return_values["output"])

    # response = await agent_chain.ainvoke(
    #     {"input": "What data do you need to create an event plan?"}
    # )
    # print(response["output"])
    #
    # response = await agent_chain.ainvoke(
    #     {"input": "Please find me the best venue for my event and catering in internet"}
    # )
    # print(response["output"])

if __name__ == '__main__':
    asyncio.run(newAgent())
