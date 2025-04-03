import requests
import json
from typing import Tuple, Optional, Dict
from app.log.logger_config import logger


class WhatsAppManager:
    def __init__(self):
        #
        pass

    def send_template_to_user(
        self, whatsapp_token: str, whatsapp_phone_number_id: str, body_template: dict
    ) -> Tuple[bool, Optional[Dict[str, str]]]:
        """
        Envía un mensaje tipo template al usuario por WhatsApp.

        Args:
            whatsapp_token (str): Token de autenticación.
            whatsapp_phone_number_id (str): ID del número de teléfono asociado a WhatsApp Business.
            body_template (dict): Cuerpo del mensaje en formato de plantilla.

        Returns:
            Tuple:
                - (True, response_json) si se envió correctamente.
                - (False, {"error": "mensaje"}) si hubo algún error.
        """
        url = f"https://graph.facebook.com/v18.0/{whatsapp_phone_number_id}/messages"

        headers = {
            "Authorization": f"Bearer {whatsapp_token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(url, headers=headers, json=body_template)
            response_data = response.json()

            if response.status_code in [200, 201]:
                logger.info(f"Plantilla enviada exitosamente: {response_data}")
                return True, response_data
            else:
                logger.error(
                    f" Error al enviar mensaje. Código {response.status_code}: {response_data}"
                )
                return False, None
        except requests.RequestException as e:
            logger.exception("Excepción al intentar enviar mensaje a WhatsApp.")
            return False, None

    def send_message_text(
        self, recipient_number:str ,whatsapp_token: str, whatsapp_phone_number_id: str, message:str
    ) -> Tuple[bool, Optional[Dict[str, str]]]:
        """
        Envía un mensaje de texto libre al usaurio

        Args:
            whatsapp_token (str): Token de autenticación.
            whatsapp_phone_number_id (str): ID del número de teléfono asociado a WhatsApp Business.
            message (str): mensaje que se enviara al usuario 

        Returns:
            Tuple:
                - (True, response_json) si se envió correctamente.
                - (False, {"error": "mensaje"}) si hubo algún error.
        """
        url = F"https://graph.facebook.com/v22.0/{whatsapp_phone_number_id}/messages"

        headers = {
            "Authorization": f"Bearer {whatsapp_token}",
            "Content-Type": "application/json",
        }
        
        payload = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_number,
        "type": "text",
        "text": {
            "body": message
        }
        })

        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response_data = response.json()

            if response.status_code in [200, 201]:
                logger.info(f"mensaje enviado exitosamente: {response_data}")
                return True, response_data
            else:
                logger.error(
                    f" Error al enviar mensaje. Código {response.status_code}: {response_data}"
                )
                return False, None
        except requests.RequestException as e:
            logger.exception("Excepción al intentar enviar mensaje a WhatsApp.")
            return False, None
