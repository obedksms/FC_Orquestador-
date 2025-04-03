import os

from dotenv import load_dotenv

from kombu import Queue

load_dotenv()

"""Obtener credenciales de RabbitMQ"""
rabbitmq_user = os.getenv("RMQ_USER")
rabbitmq_password = os.getenv("RMQ_PASSWORD")
rabbitmq_host = os.getenv("RMQ_HOST")
rabbitmq_port = os.getenv("RMQ_PORT")

""" 
Definir la URL del broker para Celery. 
RabbitMQ se usará como broker de mensajes con el protocolo `pyamqp`. 
La URL sigue el formato: pyamqp://usuario:contraseña@host:puerto//
"""
broker_url = (f"pyamqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}//")


broker_heartbeat = 10
broker_connection_timeout = 30
broker_pool_limit = None
task_acks_late = True
task_reject_on_worker_lost = True
worker_cancel_long_running_tasks_on_connection_loss = True

"""
Decidir si Celery debe reintentar conectarse al broker de mensajes cuando inicia el worker.
"""
broker_connection_retry_on_startup = True

""" 
Definir el backend de resultados. 
En este caso, `rpc://` permite que los clientes reciban los resultados de las tareas ejecutadas.
En nuestro caso en None, no es necesario
"""
result_backend = None

""" 
Definir las rutas de las tareas según la cola a la que pertenecen. 
Celery usará este mapeo para enrutar tareas a las colas correspondientes en RabbitMQ.
Nota: estas colas son internas de Celey y no son las colas por las que escucha el orquestador
estas son colas que usa Celery para delegar tareas
"""

task_queues = (
    Queue("Agente"),
    Queue("Weebhook"),
)

task_routes = {
    "worker.agent_worker.process_agente_message": {"queue": "Agente"},
    "worker.webhook_worker.process_webhook_message": {"queue": "Weebhook"},
}
