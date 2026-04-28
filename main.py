from langflow.interface.custom.custom_component import CustomComponent
from langflow.field_typing import Data
import requests

class AWSIntegrationComponent(CustomComponent):
    display_name = "AWS API Connector"
    description = "Envia dados do agente para o AWS API Gateway."

    def build_config(self):
        return {
            "url": {"display_name": "API Gateway URL", "value": "https://sua-api.execute-api.aws.com/prod/leads"},
            "payload": {"display_name": "Dados do Lead (JSON)", "multiline": True},
        }

    def build(self, url: str, payload: Data) -> Data:
        try:
            response = requests.post(url, json=payload.data)
            response.raise_for_status()
            return Data(value=response.json())
        except Exception as e:
            return Data(value={"error": str(e)})