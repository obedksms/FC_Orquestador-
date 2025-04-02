import os
import json
from typing import Optional, Literal, Tuple,Union

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.log.logger_config import logger

""" 
**Se utilizo el siguiente esquema para guardar la informacion en la base de datos**

```python
class ContactDetails(BaseModel):
    """ "Datos de contacto para hacer uso de la API de WhatsApp" """

    recipient_number: str = Field(
        ..., description="Número de WhatsApp del destinatario"
    )
    whatsapp_token: str = Field(..., description="Token de autenticación de WhatsApp")
    whatsapp_phone_number_id: str = Field(
        ..., description="ID del número de teléfono de WhatsApp"
    )
    whatsapp_business_account_id: str = Field(
        ..., description="ID de la cuenta empresarial de WhatsApp"
    )
```
```python
class MongoSchema(BaseModel):
    """ "Esquema para almacenar la solicitud de ejecución del agente y datos asociados" """

    agent_execution_id: str = Field(
        ..., description="ID de ejecución del agente Fincracks"
    )
    agent_id: str = Field(
        ..., description="ID del agente responsable de esta ejecución"
    )
    contact_details: ContactDetails = Field(
        ..., description="Detalles de contacto para el envío de mensajes"
    )
    status: Literal["send_tree", "sent_message_to_agent", "sent_message_to_user", "finish", "error"] = (
        Field("", description="Estado del proceso")
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha de creación en UTC",
        json_schema_extra={"example": "2025-03-26T12:34:56.789Z"},
    )
```

"""


# Cargar variables de entorno
load_dotenv()

_MONGODB_URL = os.getenv("MONGO_URL")
_MONGO_DB = os.getenv("MONGO_DB")
_MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION")

if not all([_MONGODB_URL, _MONGO_DB, _MONGODB_COLLECTION]):
    raise EnvironmentError("Faltan variables de entorno para la conexión a MongoDB.")


class MongoCasesManager:
    """
    Clase que maneja las operaciones con MongoDB apara recuperar datos para las ejecuciones de los workers y/o actualizar el estatos
    """

    def __init__(self):
        try:
            logger.info(f"Iniciando coneccion a DB: {self}")
            self.client = MongoClient(_MONGODB_URL)
            self.db = self.client[_MONGO_DB]
            self.collection = self.db[_MONGODB_COLLECTION]
        except PyMongoError as e:
            logger.error(f"Error de conexión a MongoDB: {e}")
            raise {"error_mongo": e}

    from typing import Tuple, Union

    def search_status_by_agent_execution_id(self, agent_execution_id: str
                                            ) -> Tuple[bool, Union[str, None, dict]]:
        """
        Busca el documento del por su ID.

        Args:
            agent_execution_id (str): ID de ejecución del agente.

        Returns:
            Tuple[bool, Union[str, None, dict]]:
                - (True, documento) si se encuentra el documento.
                - (False, None) si no se encuentra.
                - (False, {"error": "mensaje"}) si hay error en la consulta.
        """
        try:
            document = self.collection.find_one(
                {"agent_execution_id": agent_execution_id}
            )
            if document:
                return True, document
            logger.warning(f"No se encontró documento con ID: {agent_execution_id}")
            return False, None
        except PyMongoError as e:
            logger.exception(f"Error al consultar MongoDB para ID: {agent_execution_id}")
            return False, {"error": str(e)}

