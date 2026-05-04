from langflow.custom import Component
from langflow.inputs import MessageInput
from langflow.template import Output
from langflow.schema import Message
import re


class CheckPromptInjection(Component):
    display_name = "Check: Prompt Injection"
    description = "Detecta tentativas de manipulação das instruções do assistente"
    icon = "shield"

    PATTERNS = [
        r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions?",
        r"forget\s+(everything|all|your instructions)",
        r"you\s+are\s+now\s+(a|an)\s+\w+",
        r"act\s+as\s+if\s+you\s+(have\s+no|don.t\s+have)",
        r"new\s+system\s+prompt",
        r"disregard\s+(your|all|the)",
        r"jailbreak", r"DAN\b",
        r"pretend\s+you\s+(are|have\s+no)",
        r"override\s+(your\s+)?(rules|instructions|system)",
        r"ignore\s+(suas|os|as)\s+(instruções|regras|restrições)",
        r"esqueça\s+(tudo|suas instruções|as regras)",
        r"finja\s+que\s+(você|voce)\s+(é|nao|não)",
        r"novo\s+prompt\s+de\s+sistema",
    ]

    inputs = [MessageInput(name="user_input", display_name="Mensagem")]
    outputs = [Output(display_name="Resultado", name="result", method="check")]

    def check(self) -> Message:
        text = self.user_input.text if hasattr(self.user_input, "text") else str(self.user_input)
        if not text.startswith("[BLOCKED]"):
            if any(re.search(p, text, re.IGNORECASE) for p in self.PATTERNS):
                self.user_input.text = "[BLOCKED] ⚠️ Mensagem bloqueada: tentativa de manipulação detectada.\nPor favor, envie uma pergunta sobre recrutamento de TI."
        return self.user_input