import os
import json
from typing import Tuple, Optional, Dict


import pika
from dotenv import load_dotenv
from app.log.logger_config import logger

load_dotenv()

# Obtener credenciales y configuración de RabbitMQ
rabbitmq_user = os.getenv("RMQ_USER")
rabbitmq_password = os.getenv("RMQ_PASSWORD")
rabbitmq_host = os.getenv("RMQ_HOST")
rabbitmq_port = int(os.getenv("RMQ_PORT"))

# Definir colas
rabbitmq_fincracks_ejecution_queue = os.getenv("RMQ_FINCRACS_EXECUTION")
exchange = os.getenv("EXCHANGE")


class RabbitMQ:
    def __init__(self):
        try:
            self.credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, "/", self.credentials))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=rabbitmq_fincracks_ejecution_queue, durable=True)
        except Exception as e:
            raise ConnectionError(f"No se pudo conectar a RabbitMQ: {str(e)}")


    def publish_user_message_to_agent(self, user_message: str, agent_execution_id: str) -> Tuple[bool, Optional[Dict[str, str]]]:
        """
        Publica un mensaje al agente de fincracks. Usa la estructura solicitada por fincracks

        Args:
            user_message (str): Mensaje del usuario
            agent_execution_id (str): Id de la ejecucion. Util para que fincracks indentifique el proceso

        Raises:
            RuntimeError: _description_
        """
        message = {
            "payload": {
                "agent_input": {
                    "input_data": user_message,
                    "input_type": "human"
                }
            },
            "agent_execution_id": agent_execution_id,
            "event_type": "continue"
        }

        try:
            self.channel.basic_publish(
                exchange=exchange,
                routing_key=rabbitmq_fincracks_ejecution_queue,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2),
            )
            logger.info("Mensaje enviado a RabbitMQ-Fincracks")
            return True, {"message": "Mensaje enviado a RabbitMQ-Fincracks"}
        except Exception as e:
            logger.error(f"Error enviando mensaje a RabbitMQ: {str(e)}", exc_info=True)
            return False, None

    def close(self) -> None:
        """Cierra la conexión con RabbitMQ."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()        
        
