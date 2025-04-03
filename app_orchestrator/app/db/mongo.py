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

    def search_document_by_agent_execution_id(
        self,
        agent_execution_id: str
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
            logger.info(f"Iniciando busqueda para el agent_execution_id: {agent_execution_id}")
            document = self.collection.find_one(
                {"agent_execution_id": agent_execution_id}
            )
            if document:
                logger.info(document)
                return True, document
            logger.warning(f"No se encontró documento con ID: {agent_execution_id}")
            return False, None
        except PyMongoError as e:
            logger.exception(f"Error al consultar MongoDB para ID: {agent_execution_id}")
            return False, {"error": str(e)}

    def search_by_whatsapp_contact_data(
        self,
        whatsapp_business_account_id: str,
        whatsapp_phone_number_id: str,
        recipient_number: str 
        ) -> Tuple[bool, Union[str, None, dict]]:
        """
        Busca un documento en MongoDB por los datos de contacto de WhatsApp.
        Si es status es finish o error se descarta

        Args:
            whatsapp_business_account_id (str): ID de la cuenta empresarial de WhatsApp.
            whatsapp_phone_number_id (str): ID del número de teléfono de WhatsApp.
            recipient_number (str): Número de WhatsApp del destinatario (wa_id).

        Returns:
            Tuple[bool, Union[str, None, dict]]:
                - (True, agent_execution_id) si se encuentra el documento.
                - (False, None) si no se encuentra.
                - (False, {"error": "mensaje"}) si hay error en la consulta.
        """
        try:
            logger.info("Comenzando consulta a la base de datos")
            query = {
                "contact_details.whatsapp_business_account_id": whatsapp_business_account_id,
                "contact_details.whatsapp_phone_number_id": whatsapp_phone_number_id,
                "contact_details.recipient_number": recipient_number,
                "status": {"$nin": ["finish", "error"]}  # Solo documentos cuyo status NO sea 'finis' ni 'error'
            }

            document = self.collection.find_one(query)

            if document:
                agent_execution_id = document.get("agent_execution_id")
                logger.info(f"Documento encontrado. Agent Execution ID: {agent_execution_id}")
                return True, agent_execution_id

            logger.warning("No se encontró documento con los datos de contacto proporcionados.")
            return False, None

        except PyMongoError as e:
            logger.exception("Error al consultar MongoDB por datos de contacto de WhatsApp.")
            return False, {"error": str(e)}



    def search_document_by_agent_execution_id_and_return_succes(
        self,
        agent_execution_id: str
    ) -> Tuple[bool, Union[str, None, dict]]:
        """
        Busca el documento por su agent_execution_id y regresa la indicacion para continuar o denegar la operación
        "send_tree", "finish", "error"
        Se ocupa en el wroker de webhooks y tiene como obbjetivo saber si el mensaje sera recibido por el usuario
        Returns:
            Tuple:
                - (True, None) si el estatus permite continuar.
                - (False, {"warning": "mensaje"}) si no se puede continuar con el flujo.
                - (False, {"error": "mensaje"}) si hubo un error de conexión/consulta.
        """
        try:
            document = self.collection.find_one({"agent_execution_id": agent_execution_id})

            if not document:
                logger.warning(f"No se encontró documento con agent_execution_id: {agent_execution_id}")
                return False, None

            status = document.get("status", "")
            logger.info(f"Estatus encontrado para {agent_execution_id}: {status}")

            if status in ["send_tree", "finish", "error"]:
                return False, {"warning": f"No se puede procesar este mensaje. Estado actual: '{status}'"}

            return True, None

        except PyMongoError as e:
            logger.exception(f"Error al consultar MongoDB para ID: {agent_execution_id}")
            return False, {"error": str(e)}
        
    def update_status_by_agent_execution_id(
        self,
        agent_execution_id: str,
        status: str
    ) -> Tuple[bool, Union[str, None, dict]]:
        """
        Busca el documento por su agent_execution_id y actualiza el estatus de la ejecución.

        Returns:
            Tuple:
                - (True, None) si el estatus fue actualizado.
                - (False, None) si no se puede continuar con el flujo.
                - (False, {"error": mensaje}) si hubo un error en la consulta o conexión.
        """
        try:
            document = self.collection.find_one({"agent_execution_id": agent_execution_id})

            if not document:
                logger.warning(f"No se encontró documento con agent_execution_id: {agent_execution_id}")
                return False, None

            current_status = document.get("status", "")
            logger.info(f"Estatus actual de {agent_execution_id}: {current_status}")

            if current_status in ["finish", "error"]:
                logger.info(f"No se puede procesar este mensaje. Estado actual: '{current_status}'")
                return False, None

            # Actualizamos el estado
            result = self.collection.update_one(
                {"agent_execution_id": agent_execution_id},
                {"$set": {"status": status}}
            )

            if result.modified_count == 1:
                logger.info(f"Estatus actualizado a '{status}' para agent_execution_id: {agent_execution_id}")
                return True, None
            else:
                logger.warning(f"⚠️ No se modificó el documento (puede que ya tuviera el mismo estado).")
                return False, None

        except PyMongoError as e:
            logger.exception(f"Error al actualizar MongoDB para ID: {agent_execution_id}")
            return False, {"error": str(e)}
