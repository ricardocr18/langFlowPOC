from langflow.custom import Component
from langflow.inputs import MessageInput
from langflow.template import Output
from langflow.schema import Message


class ChatMultiplexer(Component):
    display_name = "Chat Multiplexer Final"
    description = "Passa mensagem de bloqueio para o Chat Output"

    inputs = [
        MessageInput(name="input_blocked", display_name="Entrada Bloqueio"),
    ]
    outputs = [
        Output(display_name="Saída", name="combined", method="output_message"),
    ]

    def output_message(self) -> Message:
        return self.input_blocked