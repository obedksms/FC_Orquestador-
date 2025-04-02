### Project Structure

```plaintext
orquestador-worker
├── app_api/
│   ├── RMQ/
│   │   └── publisher_tree.py [1.83 KB]
│   ├── db/
│   │   ├── mongo.py [4.79 KB]
│   │   └── schema_template.py [0 bytes]
│   ├── log/
│   │   └── logger_config.py [1.35 KB]
│   ├── routes/
│   │   └── tree.py [2.53 KB]
│   ├── dockerfile_api [746 bytes]
│   ├── main_api.py [562 bytes]
│   └── requirements.txt [145 bytes]
├── app_orchestrator/
│   ├── app/
│   │   ├── db/
│   │   │   └── mongo.py [3.71 KB]
│   │   ├── log/
│   │   │   └── logger_config.py [901 bytes]
│   │   ├── rabbbitMQ/
│   │   │   └── rabbitMQ.py [2.67 KB]
│   │   └── whatsapp/
│   │       ├── manager_whatsapp.py [0 bytes]
│   │       └── schema_template.py [844 bytes]
│   ├── worker/
│   │   ├── agent_worker_functions/
│   │   ├── webhook_worker_functions/
│   │   ├── agent_worker.py [3.15 KB]
│   │   ├── celery_app.py [396 bytes]
│   │   ├── celeryconfig.py [1.47 KB]
│   │   └── webhook_worker.py [1.10 KB]
│   ├── README.MD [0 bytes]
│   ├── dockerfile_orchestrator_worker [1.05 KB]
│   ├── orchestrator.py [3.62 KB]
│   ├── requirements.txt [162 bytes]
│   ├── supervisord_orchestrator.conf [492 bytes]
│   └── supervisord_workers.conf [1.32 KB]
├── logs/
│   ├── api/
│   │   ├── app_api.log [249 bytes]
│   │   ├── debug_api.log [249 bytes]
│   │   └── error_api.log [0 bytes]
│   ├── orquestador/
│   │   ├── debug_OR.log [944 bytes]
│   │   ├── error_OR.log [0 bytes]
│   │   ├── orchestrator.err.log [0 bytes]
│   │   └── orchestrator.out.log [790 bytes]
│   └── workers/
│       ├── agent_worker.err.log [305 bytes]
│       ├── agent_worker.out.log [655 bytes]
│       ├── webhook_worker.err.log [2.26 KB]
│       └── webhook_worker.out.log [657 bytes]
├── notebooks/
│   └── WA_messages.ipynb [8.46 KB]
├── README.md [1.35 KB]
└── docker-compose.yml [2.34 KB]
```


### Summary

```plaintext
Root Folder: orquestador-worker
Total Folders: 19
Total Files: 37
File Types:
  - .yml Files: 1
  - .md Files: 2
  - No Extension Files: 2
  - .py Files: 16
  - .txt Files: 2
  - .conf Files: 2
  - .log Files: 11
  - .ipynb Files: 1
Largest File: WA_messages.ipynb [8.46 KB]
Smallest File: schema_template.py [0 bytes]
Total Project Size: 50.92 KB
Ignored Files and Folders:
  - sources
  - storeMongo
```
