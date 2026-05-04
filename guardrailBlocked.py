from langflow.custom import Component
from langflow.inputs import MessageInput
from langflow.template import Output
from langflow.schema import Message  # Importação vital para compatibilidade

class GuardrailBlocked(Component):
    display_name = "Guardrail Blocked"
    description = "Retorna o motivo do bloqueio formatado corretamente para o chat."
    icon = "shield"

    inputs = [MessageInput(name="user_input", display_name="Mensagem")]
    
    # Aqui definimos o tipo de saída explicitamente como Message
    outputs = [
        Output(display_name="Resposta de Bloqueio", name="blocked", method="get_blocked")
    ]

    def get_blocked(self) -> Message:
        # Pega o texto da entrada de forma segura
        input_value = self.user_input.text if hasattr(self.user_input, "text") else str(self.user_input)

        # Se não for uma mensagem de bloqueio, interrompe a execução deste caminho
        if "[BLOCKED]" not in input_value:
            self.stop("blocked")

        # Limpa a tag técnica
        motivo = input_value.replace("[BLOCKED]", "").strip()
        
        # RETORNO CRUCIAL: Criamos um objeto Message oficial
        # Isso faz o LangFlow entender que é um dado pronto para o Chat
        return Message(text=f"🚫 Bloqueio de Segurança: {motivo}")