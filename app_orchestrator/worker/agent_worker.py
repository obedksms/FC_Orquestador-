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

print("Registrando tarea: process_agente_message")
print(app.tasks.keys())  # Verás todas las tareas registradas

@app.task(name="worker.agent_worker.process_agent_message")
def process_agent_message(message):
    logger.info(f"*************************")
    logger.info("**Iniciando worker agente**")

    """Busca en la base de dato la metadata del esa ejecucion"""
    _agent_execution_id = message.get("agent_execution_id", None)
    if not _agent_execution_id:
        logger.warning("El mensaje no contiene 'agent_execution_id'")
        logger.info(f"-------------------------------------")
        return
    succes_mongo_search, result_document = (
        mongo_manager.search_document_by_agent_execution_id(
            agent_execution_id=_agent_execution_id
        )
    )

    if not succes_mongo_search or not result_document:
        logger.info(f"-------------------------------------")
        return

    """Dado el 'event_type' se decide cual sera el siguiente paso en la ejecucion """
    _event_type = message.get("event_type")
    if not _event_type:
        logger.warning("'event_type' no encontrado en el mensaje")
        logger.info(f"-------------------------------------")
        return

    """Obtener datos de contacto y validar si existen """
    contact_details = result_document.get("contact_details", {})
    body_template = contact_details.get("body_template")
    whatsapp_token = contact_details.get("whatsapp_token")
    whatsapp_phone_number_id = contact_details.get("whatsapp_phone_number_id")
    recipient_number = contact_details.get("recipient_number")
    if any (v is None for v in [body_template,whatsapp_token,whatsapp_manager,whatsapp_phone_number_id, recipient_number,]):
        logger.warning("Datos faltantes para enviar plantilla y mensaje ")
        logger.info(f"-------------------------------------")
        return

    
    if _event_type == "template":
        """Si es 'template' tenemos que enviar la plantilla para iniciar la ventana de conversación."""
        logger.info(f"caso: template ")
        try:
            success_send_template, result = whatsapp_manager.send_template_to_user(
                whatsapp_token=whatsapp_token,
                whatsapp_phone_number_id=whatsapp_phone_number_id,
                body_template=body_template,
            )
            if success_send_template:
                mongo_manager.update_status_by_agent_execution_id(agent_execution_id=_agent_execution_id, status="sent_message_to_user")
            logger.info(f"-------------------------------------")
            return
        except Exception as e:
            logger.exception(f"Error tratando caso 'template': {e}")
            logger.info(f"-------------------------------------")
            return

    
    elif _event_type == "reply":
        """Si es 'reply' tenemos que mandar el mensaje de fincracks como un mensaje de texto simple a el usuario"""
        logger.info(f"caso: reply ")
        try:
            message_from_frincrack = message.get("message")
            succes_send_message, result = whatsapp_manager.send_message_text(
                recipient_number=recipient_number,
                whatsapp_token=whatsapp_token,
                whatsapp_phone_number_id=whatsapp_phone_number_id,
                message=message_from_frincrack    
            )
            if succes_send_message:
                mongo_manager.update_status_by_agent_execution_id(agent_execution_id=_agent_execution_id, status="sent_message_to_user")
            logger.info(f"-------------------------------------")
            return
            
        except Exception as e:
            logger.warning(f"Error:{e}")
            logger.info(f"-------------------------------------")
            return

    elif _event_type in ("end", "error"):
        """
        Para los casos de 'error' y/o 'end' el proceso ah terminado y actualizamos el estatus en la base de de datos
        """
        logger.info(f"caso: {_event_type} ")
        if _event_type == "end":
            _event_type= "finish"
    
        mongo_manager.update_status_by_agent_execution_id(agent_execution_id=_agent_execution_id, status=_event_type)
        succes_update_status = True  # simulado
        if not succes_update_status:
            logger.error("Error actualizando estado en la base")
            logger.info(f"-------------------------------------")
            return
        logger.info("Estado actualizado correctamente")

    else:
        logger.warning(f"event_type desconocido: {_event_type}")
        logger.info(f"-------------------------------------")
        return

    logger.info("Worker Agente ejecutado correctamente")

    
    