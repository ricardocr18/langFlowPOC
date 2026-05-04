from langflow.custom import Component
from langflow.inputs import MessageInput, BoolInput
from langflow.template import Output
from langflow.schema import Message
import re


class CheckOutrosIFs(Component):
    display_name = "Check: Outros IFs (Fora de Escopo)"
    description = "Detecta mensagens fora do escopo de recrutamento de TI"
    icon = "shield"

    PATTERNS = [
        r"\b(receita|cozinha|comida|culinária|bolo|jantar)\b",
        r"\b(futebol|esporte|jogo|campeonato|placar)\b",
        r"\b(política|presidente|eleição|governo|partido)\b",
        r"\b(religião|deus|oração|igreja|bíblia|alcorão)\b",
        r"\b(namoro|relacionamento|amor|sexo|namorada)\b",
        r"\b(piada|joke|humor|engraçado|funny)\b",
        r"\b(crypto|bitcoin|ethereum|investimento\s+financeiro|bolsa\s+de\s+valores)\b",
        r"\b(weather|clima|temperatura|previsão\s+do\s+tempo)\b",
        r"\b(translate|traduza|traduzir)\b",
        r"\b(harry\s+potter|star\s+wars|marvel|anime|série\s+de\s+tv)\b",
    ]

    inputs = [
        MessageInput(name="user_input", display_name="Mensagem"),
        BoolInput(name="active", display_name="Ativar verificação de escopo", value=True),
    ]
    outputs = [Output(display_name="Resultado", name="result", method="check")]

    def check(self) -> Message:
        text = self.user_input.text if hasattr(self.user_input, "text") else str(self.user_input)
        if self.active and not text.startswith("[BLOCKED]"):
            if any(re.search(p, text, re.IGNORECASE) for p in self.PATTERNS):
                self.user_input.text = (
                    "[BLOCKED] ⚠️ Mensagem fora do escopo.\n"
                    "Este assistente é um recrutador de TI. Responde apenas sobre perfis de desenvolvedores, "
                    "leads B2B de tecnologia, vagas de TI e habilidades técnicas.\n"
                    "Por favor, envie uma pergunta sobre recrutamento de TI."
                )
        return self.user_input