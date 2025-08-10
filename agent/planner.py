from typing import Any, Dict, List

# MVP sans appel LLM: heuristiques simples
async def plan_with_llm(user_msg: str, context: Dict, longterm: List[Dict], tools: List, observations: List[Dict] | None = None):
    return {
        "goals": [user_msg],
        "steps": [
            {"desc": "Chercher contexte pertinent (mémoire)", "tool": "vector_query"},
            {"desc": "Recherche web si nécessaire", "tool": "web_search"},
            {"desc": "Composer réponse", "tool": None},
        ],
    }

async def decide_next(plan: Dict, observations: List[Dict], tools: List):
    used = {o.get("action_name") for o in observations}
    if "vector_query" not in used:
        return {"kind": "tool", "name": "vector_query", "args": {"query": plan["goals"][0], "k": 5}}
    if "web_search" not in used:
        return {"kind": "tool", "name": "web_search", "args": {"query": plan["goals"][0], "top_k": 3}}
    return {"kind": "answer"}

async def compose_answer(user_msg: str, observations: List[Dict], context: Dict, longterm: List[Dict]):
    chunks = []
    for o in observations:
        if o.get("result"):
            chunks.append(str(o["result"]))
    text = "\n\n".join(chunks) or "(Aucun contexte trouvé, réponse générique)"
    return f"Réponse basée sur les éléments collectés:\n\n{text}"
