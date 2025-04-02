import os
import json
from datetime import datetime, timezone
from typing import Dict, Literal, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# from fastapi import HTTPException

from log.logger_config import logger

# Cargar variables de entorno
load_dotenv()

_MONGODB_URL = os.getenv("MONGO_URL")
_MONGO_DB = os.getenv("MONGO_DB")
_MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION")

if not all([_MONGODB_URL, _MONGO_DB, _MONGODB_COLLECTION]):
    raise EnvironmentError("Faltan variables de entorno para la conexión a MongoDB.")


class ContactDetails(BaseModel):
    """Datos de contacto para hacer uso de la API de WhatsApp"""

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
    body_template: Dict = Field(
        ...,
        description="Cuerpo de la solicitus para enviar una plantilla por la API de whatsapp",
    )


class MongoSchema(BaseModel):
    """Esquema para almacenar la solicitud de ejecución del agente y datos asociados"""

    agent_execution_id: str = Field(
        ..., description="ID de ejecución del agente Fincracks"
    )
    agent_id: str = Field(
        ..., description="ID del agente responsable de esta ejecución"
    )
    contact_details: ContactDetails = Field(
        ..., description="Detalles de contacto para el envío de mensajes"
    )
    status: Literal[
        "send_tree", "sent_message_to_agent", "sent_message_to_user", "finish", "error"
    ] = Field("", description="Estado del proceso")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha de creación en UTC",
        json_schema_extra={"example": "2025-03-26T12:34:56.789Z"},
    )


class MongoCasesManager:
    """
    Clase que maneja las operaciones con MongoDB
    """

    def __init__(self):
        try:
            logger.info(f"Iniciando coneccion a DB: {self}")
            self.client = MongoClient(_MONGODB_URL)
            self.db = self.client[_MONGO_DB]
            self.collection = self.db[_MONGODB_COLLECTION]
        except PyMongoError as e:
            logger.error(f"Error de conexión a MongoDB: {e}")
            return False, {"error_mongo": e}

    def add_item_by_agent_execution_id(self, item: MongoSchema):
        """
        Agrega un nuevo documento a la colección
        """
        try:
            result = self.collection.insert_one(item.model_dump(mode="json"))
            print(type(result))
            logger.info(f"Documento insertado con ID: {result}")
            return True, str(result.inserted_id)

        except PyMongoError as e:
            error_msg = str(e) if str(e) else repr(e)
            logger.error(f"Error al insertar documento: {error_msg}")
            return False, {"error_mongo": error_msg}

        except Exception as e:
            error_msg = (
                str(e) if str(e) else repr(e)
            )  # Return the canonical string representation of the object.
            logger.error(f"Error al insertar documento: {error_msg}")
            return False, {"error_mongo": error_msg}

    def delete_item_by_agent_execution_id(self, agent_execution_id: str):
        """
        Elimina un documento de la colección basado en su agent_execution_id
        """
        try:
            result = self.collection.delete_one(
                {"agent_execution_id": agent_execution_id}
            )

            if result.deleted_count == 1:
                logger.info(
                    f"Documento con agent_execution_id {agent_execution_id} eliminado correctamente."
                )
                return True, {"message": "Documento eliminado"}
            else:
                logger.warning(
                    f"No se encontró documento con agent_execution_id {agent_execution_id}."
                )
                return False, {"message": "Documento no encontrado"}

        except PyMongoError as e:
            error_msg = str(e) if str(e) else repr(e)
            logger.error(f"Error al eliminar documento: {error_msg}")
            return False, {"error_mongo": error_msg}

        except Exception as e:
            error_msg = str(e) if str(e) else repr(e)
            logger.error(f"Error inesperado al eliminar documento: {error_msg}")
            return False, {"error_mongo": error_msg}
