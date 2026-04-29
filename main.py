from langflow.custom import Component
from langflow.inputs import MessageInput, StrInput
from langflow.template import Output
from langflow.schema import Message
import os
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

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
        url = self.api_url or os.getenv("AWS_API_GATEWAY_URL", "")
        api_key = os.getenv("AWS_API_GATEWAY_KEY", "")
        
        lead_data = self.lead_data
        texto = lead_data.text if hasattr(lead_data, 'text') else str(lead_data)

        try:
            headers = {
                "Content-Type": "application/json",
                "x-api-key": api_key
            }
            response = requests.post(url, json={"lead_info": texto}, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"AWS HTTP error: {e.response.status_code}")
        except requests.exceptions.Timeout:
            print("AWS timeout")
        except Exception as e:
            print(f"AWS error: {str(e)}")

        return Message(text=texto)