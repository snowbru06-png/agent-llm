from .web_search import web_search
from .vector_query import vector_query
from .send_email import send_email
from pydantic import BaseModel
from typing import Callable, Any, Dict

class Tool(BaseModel):
    name: str
    description: str
    schema: Dict[str, Any]
    fn: Callable[..., Any]

TOOL_REGISTRY = [
    Tool(
        name="web_search",
        description="Recherche web (stub) – à remplacer par un vrai provider",
        schema={"type": "object", "properties": {"query": {"type": "string"}, "top_k": {"type": "integer"}}, "required": ["query"]},
        fn=web_search,
    ),
    Tool(
        name="vector_query",
        description="Recherche sémantique locale (TF-IDF MVP)",
        schema={"type": "object", "properties": {"query": {"type": "string"}, "k": {"type": "integer"}}, "required": ["query"]},
        fn=vector_query,
    ),
    Tool(
        name="send_email",
        description="Envoi d'email via SMTP",
        schema={"type": "object", "properties": {"to": {"type": "string"}, "subject": {"type": "string"}, "html": {"type": "string"}}, "required": ["to", "subject", "html"]},
        fn=send_email,
    ),
]
