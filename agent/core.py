import asyncio
from typing import Dict, Any, List

from .planner import plan_with_llm, decide_next, compose_answer
from .guardrails import enforce
from .observe import observe_and_store

MAX_STEPS = 8

async def run_agent(user_id: str, session_id: str, user_msg: str, mem, tools) -> Dict[str, Any]:
    context = mem.load_context(user_id, session_id)
    longterm = mem.retrieve_semantic(user_id, user_msg, k=6)
    plan = await plan_with_llm(user_msg, context, longterm, tools)

    observations: List[Dict[str, Any]] = []
    for step in range(MAX_STEPS):
        enforce(plan, step)
        action = await decide_next(plan, observations, tools)
        if action["kind"] == "tool":
            tool = next(t for t in tools if t.name == action["name"])  # type: ignore
            result = await asyncio.to_thread(tool.fn, **action["args"])  # sync → thread
            obs = observe_and_store(user_id, session_id, action, result, mem)
            observations.append(obs)
            plan = await plan_with_llm(user_msg, context, longterm, tools, observations)
        else:
            answer = await compose_answer(user_msg, observations, context, longterm)
            mem.maybe_persist(user_id, session_id, user_msg, answer, observations)
            return {"answer": answer, "observations": observations}

    return {"answer": "Limite d’étapes atteinte. Résumé envoyé.", "observations": observations}
