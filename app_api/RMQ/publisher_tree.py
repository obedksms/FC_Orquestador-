import os
import json
import pika
from dotenv import load_dotenv
from typing import Dict
from log.logger_config import logger

load_dotenv()

_RABBITMQ_QUEUE_PUBLISHER = os.getenv("RABBITMQ_QUEUE_PUBLISHER")
_EXCHANGE = os.getenv("EXCHANGE")
_RMQ_USER = os.getenv("RMQ_USER")
_RMQ_PASSWORD = os.getenv("RMQ_PASSWORD")
_RMQ_HOST = os.getenv("RMQ_HOST")
_RMQ_PORT = int(os.getenv("RMQ_PORT", 5672))
_RMQ_VHOST = os.getenv("RMQ_VHOST", "/")

def publish_tree(tree:Dict ={}):
    """
    Envía el árbol de ejecución al agente de Fincracks.
    """
    connection = None
    try:
        logger.info("Iniciando conexión con RabbitMQ")
        credentials = pika.PlainCredentials(_RMQ_USER, _RMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=_RMQ_HOST,
            port=_RMQ_PORT,
            virtual_host=_RMQ_VHOST,
            credentials=credentials
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue=_RABBITMQ_QUEUE_PUBLISHER, durable=True)

        logger.info(f"Publicando en la cola {_RABBITMQ_QUEUE_PUBLISHER}")
        channel.basic_publish(
            exchange=_EXCHANGE,
            routing_key=_RABBITMQ_QUEUE_PUBLISHER,
            body=json.dumps(tree),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        logger.info("Conexión cerrada, árbol publicado")
        return True, {"message": "Árbol publicado con éxito"}

    except Exception as e:
        error_msg = str(e) if str(e) else repr(e)  # Asegurar que siempre haya contenido en el error
        logger.error(f"Error al publicar en RabbitMQ: {error_msg}")
        return False, {"error_rmq": error_msg}

    finally:
        if connection and connection.is_open:
            connection.close()
