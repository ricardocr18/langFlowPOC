from langflow.custom import Component
from langflow.inputs import MessageInput, StrInput
from langflow.template import Output
from langflow.schema import Data, Message
import os
import requests


# Tenta carregar .env (opcional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # Se python-dotenv não estiver instalado, apenas segue (vai usar variáveis de ambiente do SO)
    pass

# Lê a variável de ambiente (nome: API_GATEWAY_URL)
API_GATEWAY_URL = os.getenv("AWS_API_GATEWAY_URL")

class AWSConnector(Component):
    display_name = "AWS API Connector"
    description = "Envia dados para AWS Lambda"

    inputs = [
        StrInput(
            name="api_url",
            display_name="API Gateway URL",
            value=API_GATEWAY_URL or ""
        ),
        MessageInput(
            name="lead_data",
            display_name="Dados do Lead"
        )
    ]

    outputs = [
        Output(display_name="Message", name="message", method="build_output")
    ]

    def build_output(self) -> Message:
        url = self.api_url
        lead_data = self.lead_data
        texto = lead_data.text if hasattr(lead_data, 'text') else str(lead_data)

        # Envia para AWS em background
        try:
            requests.post(url, json={"lead_info": texto}, timeout=10)
        except Exception:
            pass

        # Retorna o texto original do OpenAI para o Chat Output
        return Message(text=texto)