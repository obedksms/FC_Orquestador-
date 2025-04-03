from celery import Celery



app = Celery("orquestador")
app.config_from_object("worker.celeryconfig")

# Autodiscovery opcional (puede quedarse)
app.autodiscover_tasks(["worker.agent_worker", "worker.webhook_worker"])


# Forzar ejecución del código donde se definen las tareas
# Importaciones explícitas para asegurar el registro
#from worker import agent_worker, webhook_worker
