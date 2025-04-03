
### ✅ Variables necesarias en `.env` para este consumidor

```env
# RabbitMQ Config
RMQ_USER=tu_usuario
RMQ_PASSWORD=tu_contraseña
RMQ_HOST=localhost
RMQ_PORT=5672

# Exchange y colas
RMQ_EXCHANGE_NAME=webhook_exchange
RMQ_GLOBAL_QUEUE=global_webhook_listener
RMQ_AGENT_RESPONSE_QUEUE=agent_response_queue
```

---

### 🔍 Desglose por variable

| Variable                      | Descripción                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| `RMQ_USER`                   | Usuario de RabbitMQ                                                        |
| `RMQ_PASSWORD`               | Contraseña del usuario                                                     |
| `RMQ_HOST`                   | Host de RabbitMQ (puede ser `localhost`, `rabbitmq`, etc. según Docker)   |
| `RMQ_PORT`                   | Puerto de RabbitMQ (por defecto `5672`)                                   |
| `RMQ_EXCHANGE_NAME`          | Nombre del exchange que usas (`webhook_exchange`)                         |
| `RMQ_GLOBAL_QUEUE`           | Cola que escucha todos los webhooks (`global_webhook_listener`)           |
| `RMQ_AGENT_RESPONSE_QUEUE`   | Cola específica para respuestas del agente (`agent_response_queue`)       |

---



### Nota.
- Actualizar el readme
- Dar permisos de escrita a la carpta de logs porque el contenedor de los workers se levanta como usuario no como root
