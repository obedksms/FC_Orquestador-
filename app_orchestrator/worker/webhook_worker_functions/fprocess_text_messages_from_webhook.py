from typing import Tuple, List
from app.log.logger_config import logger

def process_text_messages_from_webhook(body_webhook: dict) -> Tuple[bool, List[str]]:
    """_summary_

    Args:
        body_webhook (dict): _description_

    Returns:
        Tuple[bool, List[str]]: _description_
    """
    try:
        text_messages = []
        entries = body_webhook.get("entry", [])
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                messages = value.get("messages", [])
                for msg in messages:
                    msg_type = msg.get("type")
                    if msg_type == "text":
                        text = msg.get("text", {}).get("body", "")
                        wa_id = msg.get("from")
                        logger.info(f"Mensaje de texto recibido de {wa_id}: {text}")
                        text_messages.append(text)
                    else:
                        logger.info(f" Mensaje ignorado, tipo no permitido: {msg_type}")
        if text_messages:
            full_message = "\n".join(text_messages)
            return True, full_message
        else:
            logger.warning("No se encontraron mensajes de tipo texto en el webhook.")
            return False, []
    except Exception as e:
        logger.exception(f"Error procesando el webhook: {e}")
        return False, []
