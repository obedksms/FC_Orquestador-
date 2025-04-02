import time
from worker.celery_app import app


from app.db.mongo import MongoCasesManager
from app.log.logger_config import logger

# Instancia principal de Celery
#app = Celery("agent_worker")


# Configurar Celery para que use el archivo `celeryconfig.py` como fuente de configuración.
#app.config_from_object("worker.celeryconfig")

_mongo = MongoCasesManager


@app.task(name="worker.agent_worker.process_agente_message")
def process_agent_message(message):

    # logger.info(f"***Mensaje del Agente recibido: {message}***")

    # """Busca en la base de dato la metadata del esa ejecucion"""
    # _agent_execution_id = message.get("agent_execution_id")
    # if not _agent_execution_id:
    #     logger.warning("El mensaje no contiene 'agent_execution_id'")
    #     return

    # succes_mongo_search, result_document = _mongo.search_status_by_agent_execution_id(
    #     agent_execution_id=_agent_execution_id
    # )

    # if not succes_mongo_search:
    #     logger.warning(f"Error al buscar en Mongo: {result_document}")
    #     return

    # if result_document is None:
    #     logger.warning(f"Documento no encontrado para: {_agent_execution_id}")
    #     return

    # """Dado el 'event_type' se decide cual sera el sigueinte paso en la ejecucion """

    # _event_type = message.get("event_type")
    # if not _event_type:
    #     logger.warning("'event_type' no encontrado en el mensaje")
    #     return

    
    
    # if _event_type == "template":
    #     """
    #     Si es 'template' tenemos que contruir el Body necesario para enviar la plantilla a partir de la metadata.
    #     Este es el primer mensaje de la ejecucion y sirve para abrir la ventaja de conversacion entre el agente y el usuario.
    #     """
    #     # succes_send_template, result = send_template(result_document)
    #     succes_send_template = True  # simulado
    #     if not succes_send_template:
    #         logger.error("Error enviando la plantilla")
    #         return
    #     logger.info("Plantilla enviada correctamente")
        
   
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
