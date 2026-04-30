from langflow.custom import Component
from langflow.inputs import MessageInput, StrInput, BoolInput
from langflow.template import Output
from langflow.schema import Message

class HITLValidator(Component):
    display_name = "HITL Validator"
    description = "Ponto de validação humana antes de executar ação"

    inputs = [
        MessageInput(name="agent_response", display_name="Resposta do Agente"),
        BoolInput(
            name="auto_approve",
            display_name="Aprovar Automaticamente",
            value=False,
            info="Ative para bypassar a validação humana (testes)"
        ),
        StrInput(
            name="approval_keyword",
            display_name="Palavra de Aprovação",
            value="APROVAR",
            info="Usuário deve incluir essa palavra para aprovar"
        ),
        StrInput(
            name="rejection_keyword",
            display_name="Palavra de Rejeição",
            value="REPROVADO",
            info="Usuário deve incluir essa palavra para reprovar"
        )
    ]

    outputs = [
        Output(display_name="Resultado", name="resultado", method="get_resultado")
    ]

    def _extract_text(self) -> str:
        msg = self.agent_response
        return msg.text if hasattr(msg, 'text') else str(msg)

    def _is_approved(self) -> bool:
        if self.auto_approve:
            return True
        return self.approval_keyword.upper() in self._extract_text().upper()

    def _is_rejected(self) -> bool:
        return self.rejection_keyword.upper() in self._extract_text().upper()

    def get_resultado(self) -> Message:
        texto = self._extract_text()
        if self._is_approved():
            return Message(text=f"✅ APROVADO — Lead enviado para AWS!\n\n{texto}")
        elif self._is_rejected():
            return Message(text=f"❌ REPROVADO — Lead descartado.\n\n{texto}")
        else:
            return Message(
                text=f"⏳ AGUARDANDO APROVAÇÃO HUMANA\n\n"
                     f"Resposta do agente:\n{texto}\n\n"
                     f"➡ Para aprovar: **{self.approval_keyword}**\n"
                     f"➡ Para reprovar: **{self.rejection_keyword}**"
            )