import time

from worker.celery_app import app

from app.log.logger_config import logger
from worker.webhook_worker_functions.fprocess_text_messages_from_webhook import (process_text_messages_from_webhook,)
from worker.webhook_worker_functions.fextract_whatsapp_contact_data import (extract_whatsapp_contact_data,)
from app.rabbbitMQ.rabbitmq import RabbitMQ
from app.db.mongo import MongoCasesManager

mongo_manager = MongoCasesManager()
rabbitmq_manager = RabbitMQ()

# Tarea: Procesar mensaje de Webhook
@app.task(
    name="worker.webhook_worker.process_webhook_message"
)  # --> Celery necesita el nombre registrado de la tarea, no solo el nombre de la función.
def process_webhook_message(body_webhook):
    """Verificar si el mensaje del webhook es de tipo texto"""
    success, messages = process_text_messages_from_webhook(body_webhook=body_webhook)
    if not success:
        # TODO Enviar menasaje de advertencia al usuario sobre responer solo con tipo texto
        return

    """Extraer del webhook los datos necesarios par identificarlo en la DB"""
    logger.info("extraer datos del webhook para unciar busqueda en la DB.")
    success, contact_data = extract_whatsapp_contact_data(body_webhook)
    if not success:
        logger.warning("No se pudieron extraer los datos de contacto del webhook.")
        return

    """Buscar en la base de datos y extraer el agent_execution_id si existe"""
    # Ahora puedes consultar en Mongo
    success, agent_execution_id_from_db = mongo_manager.search_by_whatsapp_contact_data(
        whatsapp_business_account_id=contact_data["whatsapp_business_account_id"],
        whatsapp_phone_number_id=contact_data["whatsapp_phone_number_id"],
        recipient_number=contact_data["recipient_number"],
    )
    if not success:
        logger.warning(
            "No se contro egent_execution _id asociado a este webhook, se descarta mensaje"
        )
        return

    """Si tenemos agent_execution_id buscamos en la base de datos el status de ejcucion del agente, si es finish o error, se descarta el mensaje"""
    succes, result = (
        mongo_manager.search_document_by_agent_execution_id_and_return_succes(
            agent_execution_id=agent_execution_id_from_db
        )
    )

    if not succes:
        logger.warning(
            f"No se puede continuar con el proceso porque el estatus de la operacion actual para el agent_execution_id: {agent_execution_id_from_db} es {result}"
        )
        return

    """Enviar mensaje a fincracks"""
    succes, result = rabbitmq_manager.publish_user_message_to_agent(
        user_message=messages, agent_execution_id=agent_execution_id_from_db
    )

    """Actualizar status en la base de datos"""
    if succes:
        succes, result = mongo_manager.update_status_by_agent_execution_id(
            agent_execution_id=agent_execution_id_from_db,
            status="sent_message_to_agent",
        )
