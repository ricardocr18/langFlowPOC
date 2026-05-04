from langflow.custom import Component
from langflow.inputs import MessageInput
from langflow.template import Output
from langflow.schema import Message
import re


class CheckOfensas(Component):
    display_name = "Check: Ofensas"
    description = "Detecta linguagem ofensiva ou ameaças"
    icon = "shield"

    PATTERNS = [
        r"\bputa\b", r"\bmerda\b", r"\bviado\b", r"\bidiota\b", r"\bestupido\b",
        r"\bcretino\b", r"\bimbecil\b", r"\bvagabundo\b", r"\bbosta\b",
        r"\bfoda[- ]?se\b", r"\bporra\b", r"\bcacete\b", r"\bburro\b",
        r"\bfuck\b", r"\bshit\b", r"\basshole\b", r"\bbitch\b", r"\bstupid\b",
        r"\bidiot\b", r"\bmoron\b", r"\bdumbass\b",
        r"\b(vou|irei|vamos)\s+(te|você|voce)\s+(matar|destruir|acabar)",
        r"\b(kill|destroy|hack|attack)\s+you\b",
    ]

    inputs = [MessageInput(name="user_input", display_name="Mensagem")]
    outputs = [Output(display_name="Resultado", name="result", method="check")]

    def check(self) -> Message:
        text = self.user_input.text if hasattr(self.user_input, "text") else str(self.user_input)
        if not text.startswith("[BLOCKED]"):
            if any(re.search(p, text, re.IGNORECASE) for p in self.PATTERNS):
                self.user_input.text = "[BLOCKED] ⚠️ Mensagem bloqueada: linguagem inadequada detectada.\nPor favor, mantenha a conversa respeitosa."
        return self.user_input