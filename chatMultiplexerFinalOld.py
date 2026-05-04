"""
Esse código dá opção para o Chat Output receber mensagens tanto do fluxo
normal (aprovado pelo HITL/Agent) quanto do fluxo de bloqueio
(quando o guardrail é acionado). Ele verifica as entradas
em ordem de prioridade: primeiro a mensagem aprovada,
depois a mensagem bloqueada. Se nenhuma das entradas tiver texto válido,
ele retorna uma mensagem padrão indicando que o sistema processou
a solicitação, mas não gerou uma resposta específica.
"""

from langflow.custom import Component
from langflow.inputs import MessageInput
from langflow.template import Output
from langflow.schema import Message


class ChatMultiplexer(Component):
    display_name = "Chat Multiplexer Final"
    description = "Unifica saída do fluxo normal e do guardrail para o Chat Output"

    inputs = [
        MessageInput(name="input_blocked", display_name="Entrada Bloqueio"),
        MessageInput(name="input_approved", display_name="Entrada Aprovada"),
    ]
    outputs = [
        Output(display_name="Saída", name="combined", method="output_message"),
    ]

    def output_message(self) -> Message:
        # Fluxo normal (mensagem aprovada pelo HITL/Agent)
        if self.input_approved:
            txt = getattr(self.input_approved, "text", "")
            if txt and txt.strip():
                return self.input_approved  # ← retorna original com session_id

        # Fluxo bloqueado (guardrail disparou)
        if self.input_blocked:
            txt = getattr(self.input_blocked, "text", "")
            if txt and txt.strip():
                return self.input_blocked   # ← retorna original com session_id

        return Message(text="Sistema processou, mas não gerou resposta.")