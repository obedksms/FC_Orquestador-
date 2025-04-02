from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class TextParameter(BaseModel):
    type: Literal["text"] = "text"
    parameter_name: str = Field(..., regex=r"^[a-z0-9_]+$")
    text: str

class Language(BaseModel):
    code: str  # e.g., "es_MX"

class BodyComponent(BaseModel):
    type: Literal["body"] = "body"
    parameters: List[TextParameter]

class TemplatePayload(BaseModel):
    name: str  # nombre de la plantilla aprobada en WhatsApp
    language: Language
    components: List[BodyComponent]

class WhatsAppTemplateMessage(BaseModel):
    messaging_product: Literal["whatsapp"] = "whatsapp"
    recipient_type: Literal["individual"] = "individual"
    to: str  # número en formato internacional
    type: Literal["template"] = "template"
    template: TemplatePayload
