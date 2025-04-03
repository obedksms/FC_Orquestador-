from celery import Celery



app = Celery("orquestador")
app.config_from_object("worker.celeryconfig")

# Autodiscovery opcional (puede quedarse)
app.autodiscover_tasks(["worker.agent_worker", "worker.webhook_worker"])


from worker import agent_worker, webhook_worker