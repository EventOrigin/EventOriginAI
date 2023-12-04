import os
import asyncio
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.agents import Tool, initialize_agent, AgentType, load_tools
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun, E2BDataAnalysisTool, HumanInputRun
from langchain.utilities.google_serper import GoogleSerperAPIWrapper
from langchain_core.messages import SystemMessage

from Models.Model import event, contacts
from Prompts.SystemPrompt import (super_prompt, default_context)
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory

os.environ["OPENAI_API_KEY"] = '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'
os.environ["SERPER_API_KEY"] = '29ce322a9d04ab78fc16d78f2caea4a40664670d'
# os.environ["E2B_API_KEY"] = 'e2b_e13d23d507cf8b524363d563a0eec57be35019ff'
search = GoogleSerperAPIWrapper()
# DuckDuckGoSearchRun(),
# tools = [Tool(name="Intermediate Answer", func=search.run, description="use for search in internet",)]
memory = ConversationBufferMemory(memory_key="chat_history", input_key='input', output_key="output")
# memory = ConversationBufferWindowMemory(memory_key="chat_history",input_key="input",output_key='output', return_messages=True, k=4)

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
    agent_kwargs = {
        'format_instructions': super_prompt
    }

    llm = ChatOpenAI(temperature=0.5, model_name="gpt-4-1106-preview")
    # tools = load_tools(["google-serper"], llm=llm)
    tools = [DuckDuckGoSearchRun(), HumanInputRun(input_func=get_input)]
    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
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
        {"input": "What data do you need to create an event plan?"}
    )
    print(response["output"])

    response = await agent_chain.ainvoke(
        {"input": "Please find me the best venue for my event and catering in internet"}
    )
    print(response["output"])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(newAgent())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
