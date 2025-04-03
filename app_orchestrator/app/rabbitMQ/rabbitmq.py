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
        pass   

    def publish_user_message_to_agent(self, user_message: str, agent_execution_id: str) -> Tuple[bool, Optional[Dict[str, str]]]:
        """
        Publica un mensaje del usuario en la cola de RabbitMQ correspondiente al agente.

        Esta función establece una conexión con RabbitMQ y publica un mensaje estructurado que
        contiene la entrada del usuario y el ID de ejecución del agente. El mensaje se envía a
        una cola específica para su posterior procesamiento por parte del agente.

        Args:
            user_message (str): Mensaje de entrada proporcionado por el usuario.
            agent_execution_id (str): Identificador único de la ejecución del agente asociado.

        Returns:
            Tuple[bool, Optional[Dict[str, str]]]: 
                - True y None si el mensaje fue publicado exitosamente.
                - False y None si ocurrió un error durante el proceso.
        """
        logger.info("Conectado con RabbitMQ")
        credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=rabbitmq_host,
                port=rabbitmq_port,
                virtual_host="/",
                credentials=credentials,
                heartbeat=0,
                blocked_connection_timeout=10,
                connection_attempts=3,
                retry_delay= 3,
                socket_timeout= 10
            ))
        channel = connection.channel()
        channel.queue_declare(queue=rabbitmq_fincracks_ejecution_queue, durable=True)
        
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
            logger.info("Publicando mensaje")
            channel.basic_publish(
                exchange=exchange,
                routing_key=rabbitmq_fincracks_ejecution_queue,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2),
            )
            
            logger.info("Mensaje enviado a RabbitMQ")
            logger.info("Cerando conexion con RabbitMQ")
            connection.close()
            
            return True, None
        except Exception as e:
            logger.error(f"Error enviando mensaje a RabbitMQ: {str(e)}", exc_info=True)
            if connection and not connection.is_closed:
                connection.close()   
            return False, None

    