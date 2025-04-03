import os
import sys
import signal
import json

import pika
from dotenv import load_dotenv

from worker.agent_worker import process_agent_message
from worker.webhook_worker import process_webhook_message
from app.log.logger_config import logger
load_dotenv()

# Obtener credenciales y configuración de RabbitMQ
rabbitmq_user = os.getenv("RMQ_USER")
rabbitmq_password = os.getenv("RMQ_PASSWORD")
rabbitmq_host = os.getenv("RMQ_HOST")
rabbitmq_port = int(os.getenv("RMQ_PORT"))

# Definir Exchange y colas
rabbitmq_exchange_name = os.getenv("RMQ_EXCHANGE_NAME")
rabbitmq_global_queue= os.getenv("RMQ_GLOBAL_QUEUE")
rabbitmq_agent_response_queue = os.getenv("RMQ_AGENT_RESPONSE_QUEUE")

# Configurar la conexión a RabbitMQ
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
parameters = pika.ConnectionParameters(
    host=rabbitmq_host, port=rabbitmq_port, credentials=credentials
)

try:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    logger.info("✅ Conexión establecida con RabbitMQ")
except Exception as e:
    logger.error(f"❌ Error al conectar con RabbitMQ: {e}")
    sys.exit(1)

# Declarar el exchange (topic)
#channel.exchange_declare(exchange=rabbitmq_exchange_name, exchange_type="topic")
channel.exchange_declare(exchange=rabbitmq_exchange_name, exchange_type="topic", durable=True)

# Declarar la cola global para escuchar todos los webhooks
channel.queue_declare(queue=rabbitmq_global_queue, durable=True)
channel.queue_bind(exchange=rabbitmq_exchange_name, queue=rabbitmq_global_queue, routing_key="webhook.#")

# Declarar la cola específica para tareas
channel.queue_declare(queue=rabbitmq_agent_response_queue, durable=True)

def callback_global(ch, method, properties, body):
    """Callback para la cola global"""
    message = json.loads(body.decode())
    logger.info(f"Mensaje recibido en {rabbitmq_global_queue}: {message}")
    try:
        #logger.info(f"📥 [Global] Mensaje recibido: {body.decode()}")
        # Procesar mensaje aquí...
        process_webhook_message.apply_async(args=[message], queue="Weebhook")
        logger.info("Tarea enviada al worker")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"[Global] Error procesando mensaje: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def callback_task(ch, method, properties, body):
    """Callback para la cola de tareas"""
    try:
        logger.info(f"Mensaje recibido en {rabbitmq_agent_response_queue}: {body.decode()}")
        message = json.loads(body.decode())
        process_agent_message.apply_async(args=[message], queue="Agente")
        logger.info("* Tarea enviada al worker {}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"[Tarea] Error enviando tarea: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def graceful_shutdown(signal, frame):
    logger.info("* Apagando orquestador...")
    channel.stop_consuming()
    connection.close()
    sys.exit(0)

# Registrar manejadores de señales
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

# Suscribirse a las colas
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=rabbitmq_global_queue, on_message_callback=callback_global, auto_ack=False)
channel.basic_consume(queue=rabbitmq_agent_response_queue, on_message_callback=callback_task, auto_ack=False)

logger.info("** Orquestador escuchando **")
channel.start_consuming()
