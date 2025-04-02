import time

from worker.celery_app  import app

from app.log.logger_config import logger

"""Instancia principal de Celery"""
#app = Celery("webhook_worker")
#app.config_from_object("worker.celeryconfig")


# Tarea: Procesar mensaje de Webhook
@app.task(name="worker.webhook_worker.process_webhook_message") # --> Celery necesita el nombre registrado de la tarea, no solo el nombre de la función.
def process_webhook_message(message):
    logger.info(f"📩 Mensaje de Webhook recibido: {message}")
    # Recibe un mensaje a travez de un Webhook de meta.
    # Autorizacion: Busca en la base de datos si el mensaje entrante dada su metadata se encuetra en proceso y/o ejecucion de lo contrario sera descartado
    # Clasificador: Solo admite el tipo de menasje de texto, los demas seran descartados (audio, ubicacion, video, imagen)
    # Una vez que obtiene el mensaje lo publica en la cola correspondiente para ser consumido por el Agente (mensaje con la estrucuta requerida por fincracks)
    # Actualiza el estatus en la base de datos
    time.sleep(2)
    logger.info("✅ Worker Webhook ejecutado")