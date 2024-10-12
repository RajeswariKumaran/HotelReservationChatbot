from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory
from handlers.chat_model_start_handler import ChatModelStartHandler
from dotenv import load_dotenv

from tools.reservation import reserve_hotel_tool

load_dotenv()

handler  = ChatModelStartHandler()
# Initialize LLM
chat = ChatOpenAI(
    callbacks=[handler]
)

# Initial prompt used to greet and ask about reservation
greeting_prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
            "You are an AI that can reserve rooms in hotel\n"
            "Greet the user with welcome message 'Hello! Welcome to Ronitha Inns! Do you have a reservation?'"
        )),
        MessagesPlaceholder(variable_name = "chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name = "agent_scratchpad")

    ]
)

# Prompt used to collect details regarding reservation subsequent to request for reservation
reservation_prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
            "You are an AI that can reserve rooms in hotel\n"
            "First, greet the user with welcome message 'Hello! Welcome to Ronitha Inns! Do you have a reservation?'"
            "If the user answers 'Yes' to the first question, thank the answer and stop conversation"
            "If the user answers 'No' then ask for all the information required only one after another "
            "until all aspects as given in the 'reserve_room' \n"
            "tool are obtained from the user in exact same order"
            "While asking for check in and check out dates ask for YYYY-MM-DD format \n"
            "While asking for the type of room give options of Single, Deluxe, Executive, Suite. \n"
            "Validate all inputs with tool 'reserve_room' before confirmation to reserve. Do not make assumptions on data validity. \n"
            "Before reservation, display all the details collected and ask for confirmation"
        )),
        MessagesPlaceholder(variable_name = "chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name = "agent_scratchpad")
    ]
)

# Memory to hold summary of conversations 
memory = ConversationBufferMemory(memory_key = "chat_history", return_messages = True)

# Tool to validate information in hotel reservation
tools = [
    reserve_hotel_tool
]

# Agent for greeting
# greeting_agent = OpenAIFunctionsAgent(
#     llm=chat,
#     prompt=greeting_prompt,
#     tools = tools
# )

# Agent executor for greeting
# greeting_agent_executor = AgentExecutor(
#     agent=greeting_agent,
#     # verbose=True,
#     tools=tools,
#     memory=memory
# )

# Agent for reservation
reservation_agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=reservation_prompt,
    tools = tools
)

# Agent executor for reservation
reservation_agent_executor = AgentExecutor(
    agent=reservation_agent,
    # verbose=True,
    tools=tools,
    memory=memory
)

# First invoke greeting and ask for reservation
# result = greeting_agent_executor("Hello, ask me whether I have a reservation\n")
# print(result['output'])

# Continuous conversation with user to collect details regarding reservation
continue_chat = True
while continue_chat:
    content = input("\n>> ")
    if content.lower() in ["end chat", "bye", "goodbye"]: 
        continue_chat = False
        break
    result = reservation_agent_executor(content)
    print(result['output'])
