from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from agent.core import run_agent
from agent.mem import MemoryStore
from agent.tools import TOOL_REGISTRY

load_dotenv()
app = FastAPI(title="Agent LLM API")
mem_store = MemoryStore()

class Msg(BaseModel):
    user_id: str
    session_id: str
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(msg: Msg):
    result = await run_agent(
        user_id=msg.user_id,
        session_id=msg.session_id,
        user_msg=msg.message,
        mem=mem_store,
        tools=TOOL_REGISTRY,
    )
    return result
