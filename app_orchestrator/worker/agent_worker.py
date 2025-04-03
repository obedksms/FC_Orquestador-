import time
import json
from worker.celery_app import app


from app.db.mongo import MongoCasesManager
from app.log.logger_config import logger
from app.whatsapp.whatsapp_manager import WhatsAppManager

# Instancia principal de Celery
# app = Celery("agent_worker")


# Configurar Celery para que use el archivo `celeryconfig.py` como fuente de configuración.
# app.config_from_object("worker.celeryconfig")

mongo_manager = MongoCasesManager()
whatsapp_manager = WhatsAppManager()


@app.task(name="worker.agent_worker.process_agente_message")
def process_agent_message(message):

    logger.info(f"Mensaje del Agente recibido:{message}")

    """Busca en la base de dato la metadata del esa ejecucion"""

    # Verificar que el mensaje tenga agent_execution_id
    _agent_execution_id = message.get("agent_execution_id", None)
    if not _agent_execution_id:
        logger.warning("El mensaje no contiene 'agent_execution_id'")
        return
    # Buscar documento en Mongo
    succes_mongo_search, result_document = (
        mongo_manager.search_document_by_agent_execution_id(
            agent_execution_id=_agent_execution_id
        )
    )

    if not succes_mongo_search or not result_document:
        return

    """Dado el 'event_type' se decide cual sera el sigueinte paso en la ejecucion """
    # Verificar que venga event_type
    _event_type = message.get("event_type")
    if not _event_type:
        logger.warning("'event_type' no encontrado en el mensaje")
        return

    if _event_type == "template":
        """
        Si es 'template' tenemos que enviar la plantilla para iniciar la ventana de conversacion.
        """
        result_document = json.dumps(result_document)
        contact_details = result_document.get("contact_details", {})
        body_template = contact_details.get("body_template")
        whatsapp_token = contact_details.get("whatsapp_token")
        whatsapp_phone_number_id = contact_details.get("whatsapp_phone_number_id")

        succes_send_template, result = whatsapp_manager.send_template_to_user(
            whatsapp_token=whatsapp_token,
            whatsapp_phone_number_id=whatsapp_phone_number_id,
            body_template=body_template,
        )

        if not succes_send_template:
            return
        logger.info("Plantilla enviada correctamente")


    # elif _event_type == "reply":
    #     """
    #     Si es 'reply' tenemos que enviar un mensaje de texto simple
    #     """
    #     # succes_send_message, result = send_message(result_document)
    #     succes_send_message = True  # simulado
    #     if not succes_send_message:
    #         logger.error("Error enviando mensaje")
    #         return
    #     logger.info("Mensaje enviado correctamente")

    # elif _event_type in ("end", "error"):
    #     """
    #     Para los casos de 'error' y/o 'end' el proceso ah terminado y actualizamos el estatus en la base de de datos
    #     """
    #     # succes_update_status, result = update_status(...)
    #     succes_update_status = True  # simulado
    #     if not succes_update_status:
    #         logger.error("Error actualizando estado en la base")
    #         return
    #     logger.info("Estado actualizado correctamente")

    # else:
    #     logger.warning(f"event_type desconocido: {_event_type}")
    #     return

    logger.info("Worker Agente ejecutado correctamente")
