from datetime import datetime
from typing import Dict, Any

def observe_and_store(user_id: str, session_id: str, action: Dict[str, Any], result: Any, mem):
    obs = {
        "ts": datetime.utcnow().isoformat(),
        "action_name": action.get("name"),
        "args": action.get("args"),
        "result": result,
    }
    mem.store_episode(user_id, session_id, obs)
    return obs
