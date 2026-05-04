from langflow.custom import Component
from langflow.inputs import MessageInput
from langflow.template import Output
from langflow.schema import Message


class GuardrailSafe(Component):
    display_name = "Guardrail Safe"
    description = "Passa a mensagem para o Agent somente se não for bloqueada"
    icon = "shield"

    inputs = [MessageInput(name="user_input", display_name="Mensagem")]
    outputs = [Output(display_name="Para o Agent", name="safe", method="get_safe")]

    def get_safe(self) -> Message:
        text = self.user_input.text if hasattr(self.user_input, "text") else str(self.user_input)
        if text.startswith("[BLOCKED]"):
            self.stop("safe")
        return self.user_input