from fastapi import APIRouter, HTTPException, Request, Depends
from db.mongo import MongoCasesManager, MongoSchema, ContactDetails
from RMQ.publisher_tree import publish_tree
from log.logger_config import logger
from pydantic import BaseModel, Field
from typing import Any, Dict


router = APIRouter()

# Dependency injection
mongo_manager = MongoCasesManager()


def get_mongo_manager():
    return mongo_manager


# Pydantic schema
class SchemaTree(BaseModel):
    tree: Dict[str, Any] = Field(..., description="Árbol del agente Fincracks")
    contact_details: Dict[str, Any] = Field(..., description="Datos de contacto de WhatsAPP ")


@router.post("/tree")
async def save_and_send_tree(
    request: SchemaTree, mongo: MongoCasesManager = Depends(get_mongo_manager)
):
    _tree = request.tree
    _contacdetails = request.contact_details
    
    # Validar campos requeridos
    required_fields = ["agent_execution_id", "agent_id"]
    missing_fields = [field for field in required_fields if field not in _tree]
    if missing_fields:
        logger.warning(f"Campos faltantes: {missing_fields}")
        raise HTTPException(
            status_code=422, detail=f"Faltan los campos: {', '.join(missing_fields)}"
        )
    # Validar estructura del contacto
    try:
        contact = ContactDetails(**_contacdetails)
    except Exception as e:
        logger.error(f"Error al validar 'contact_details': {str(e)}")
        raise HTTPException(
            status_code=422, detail="Estructura inválida en 'contact_details'"
        )

    logger.info("Datos recibidos validados")

    # Crear schema para guardar
    mongo_data = MongoSchema(
        agent_execution_id=_tree["agent_execution_id"],
        agent_id=_tree["agent_id"],
        contact_details=contact,
        status="send_tree",
    )

    # Insertar en Mongo
    logger.info("Guardando datos en BD")
    success, message = mongo.add_item_by_agent_execution_id(mongo_data)
    if not success:
        raise HTTPException(status_code=500, detail=message)
    
    # Enviamos arbol a la cola de fincracks
    logger.info("Iniciando proceso de publicacion")
    success, message = publish_tree(tree=_tree)
    if not success:
        #En caso de error borramos de la base de datos el item 
        success, message = mongo.delete_item_by_agent_execution_id(agent_execution_id=_tree["agent_execution_id"])
        raise HTTPException(status_code=500, detail=message)

    return {
        "status": True,
        "message": "start_process"
    }
