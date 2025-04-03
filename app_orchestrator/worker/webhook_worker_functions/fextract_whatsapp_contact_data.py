import re
from typing import Tuple, Optional, Dict

from app.log.logger_config import logger



def extract_whatsapp_contact_data(body_webhook: dict) -> Tuple[bool, Optional[Dict[str, str]]]:
    """
    Extrae el ID de cuenta de WhatsApp, phone_number_id y el wa_id del remitente (from).

    Args:
        body_webhook (dict): Cuerpo del webhook recibido.

    Returns:
        Tuple:
            - (True, data) si la extracción fue exitosa.
            - (False, None) si hubo error o faltan campos.
    """
    try:
        
        entry = body_webhook.get("entry", [])[0]
        whatsapp_business_account_id = entry.get("id")
        logger.info(f"whatsapp_business_account_id:{whatsapp_business_account_id}")
        
        change = entry.get("changes", [])[0]
        value = change.get("value", {})
        phone_number_id = value.get("metadata", {}).get("phone_number_id")
        logger.info(f"phone_number_id:{phone_number_id}")

        message = value.get("messages", [])[0]
        from_wa_id = message.get("from")
        #from_wa_id= 5219531127188
        #pero en mi base de datos se guardo como : +529531127188 
        from_wa_id = normalize_phone_number(from_wa_id)
        
        logger.info(f"from_wa_id:{from_wa_id}")
        if whatsapp_business_account_id and phone_number_id and from_wa_id:
            return True, {
                "whatsapp_business_account_id": whatsapp_business_account_id,
                "whatsapp_phone_number_id": phone_number_id,
                "recipient_number": from_wa_id
            }

        logger.warning(" No se pudieron extraer los datos necesarios del webhook.")
        return False, None

    except Exception as e:
        logger.exception("Error al extraer datos del webhook")
        return False, None




def normalize_phone_number(number: str) -> str:
    """
    Normaliza números de WhatsApp al formato internacional mexicano +52xxxxxxxxxx,
    eliminando el dígito 1 si es necesario (usado en móviles mexicanos).

    Args:
        number (str): Número original (puede venir como '521...', '1...', '953...', etc.)

    Returns:
        str: Número normalizado en formato +52XXXXXXXXXX
    """
    if not number:
        return ""

    # Quitar todo excepto números
    number = re.sub(r"\D", "", number)

    # Si empieza con '521' o '1' y tiene 11 dígitos, eliminar el '1'
    if number.startswith("521") and len(number) == 13:
        return f"+52{number[3:]}"
    elif number.startswith("1") and len(number) == 11:
        return f"+52{number[1:]}"
    elif len(number) == 10:
        return f"+52{number}"
    elif number.startswith("52") and len(number) == 12:
        return f"+52{number[2:]}"  # quitar el 52 y volver a ponerlo para mantener formato limpio

    # Fallback conservador
    return f"+{number}"