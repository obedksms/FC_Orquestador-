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
│   │   │   └── mongo.py [9.20 KB]
│   │   ├── log/
│   │   │   └── logger_config.py [1006 bytes]
│   │   ├── rabbitMQ/
│   │   │   └── rabbitmq.py [4.59 KB]
│   │   └── whatsapp/
│   │       └── whatsapp_manager.py [3.57 KB]
│   ├── worker/
│   │   ├── agent_worker_functions/
│   │   ├── webhook_worker_functions/
│   │   │   ├── fextract_whatsapp_contact_data.py [2.82 KB]
│   │   │   └── fprocess_text_messages_from_webhook.py [1.45 KB]
│   │   ├── __init__.py [0 bytes]
│   │   ├── agent_worker.py [5.08 KB]
│   │   ├── celery_app.py [397 bytes]
│   │   ├── celeryconfig.py [1.67 KB]
│   │   └── webhook_worker.py [3.26 KB]
│   ├── README.MD [0 bytes]
│   ├── dockerfile_orchestrator_worker [1.05 KB]
│   ├── orchestrator.py [3.59 KB]
│   ├── requirements.txt [162 bytes]
│   ├── supervisord_orchestrator.conf [541 bytes]
│   └── supervisord_workers.conf [1.90 KB]
├── notebooks/
│   ├── WA_messages.ipynb [9.13 KB]
│   └── dic converter.ipynb [2.41 KB]
├── sources/
│   ├── excalidraw/
│   │   ├── architecture-diagram-components.excalidrawlib [95.81 KB]
│   │   ├── wroker_from_agent.excalidraw [51.95 KB]
│   │   └── wroker_from_webhook.excalidraw [56.43 KB]
│   └── schemas/
│       ├── api_request/
│       │   ├── api_tree_obed_ksms.json [17.49 KB]
│       │   └── api_tree_obed_personal.json [17.45 KB]
│       ├── webhooks/
│       │   ├── all.txt [7.57 KB]
│       │   ├── audio.json [1.63 KB]
│       │   ├── contacts.json [2.15 KB]
│       │   ├── document.json [1.64 KB]
│       │   ├── encuesta.json [1.83 KB]
│       │   ├── foto.json [1.57 KB]
│       │   ├── imagen_and_text.json [1.64 KB]
│       │   ├── location.json [1.48 KB]
│       │   ├── message_text.json [1.43 KB]
│       │   ├── message_text_whit_json.json [1.43 KB]
│       │   ├── sticker.json [1.63 KB]
│       │   └── webhook_ksms.json [299 bytes]
│       ├── contact_details.json [1.53 KB]
│       ├── create_body_template_text_based.json [914 bytes]
│       ├── message_from_fincraks.json [384 bytes]
│       ├── response_format_fincracks.json [211 bytes]
│       ├── send_body_template_text_based.json [761 bytes]
│       └── tree.json [14.52 KB]
├── README.md [1.35 KB]
├── docker-compose.yml [2.34 KB]
└── folder-structure.md [3.77 KB]
```


### Summary

```plaintext
Root Folder: orquestador-worker
Total Folders: 20
Total Files: 53
File Types:
  - .yml Files: 1
  - .md Files: 3
  - No Extension Files: 2
  - .py Files: 18
  - .txt Files: 3
  - .conf Files: 2
  - .ipynb Files: 2
  - .excalidrawlib Files: 1
  - .excalidraw Files: 2
  - .json Files: 19
Largest File: architecture-diagram-components.excalidrawlib [95.81 KB]
Smallest File: schema_template.py [0 bytes]
Total Project Size: 352.87 KB
Ignored Files and Folders:
  - logs
  - storeMongo
```
