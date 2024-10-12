from typing import Any, Dict, List
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from pyboxen import boxen

# Function to print boxes around human, user and system messages during conversation
def boxen_print(*args, **kwargs):
    print(boxen(*args, **kwargs))

# on_chat_model_start is run when LLM starts running
class ChatModelStartHandler(BaseCallbackHandler):
    def on_chat_model_start(self, serialized, messages, **kwargs):
        print("\n\n========Sending Messages=========\n\n")

        for message in messages[0]:
            if message.type == "system":
                boxen_print(message.content, title=message.type, color="blue")

            elif message.type == "human":
                boxen_print(message.content, title=message.type, color="yellow")

            elif message.type == "ai" and "function_call" in message.additional_kwargs:
                call = message.additional_kwargs["function_call"]
                boxen_print(f"Running tool {call['name']} with args {call['arguments']}", title=message.type, color="red")

            elif message.type == "ai":
                boxen_print(message.content, title="Reservation Assistant", color="cyan")

            elif message.type == "function":
                boxen_print(message.content, title=message.type, color="blue")

            else:
                boxen_print(message.content, title=message.type)