from __future__ import annotations
from typing import Dict, List, Any
import json, pathlib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_DIR = pathlib.Path(".data")
DATA_DIR.mkdir(exist_ok=True)

class MemoryStore:
    def __init__(self):
        self.session_ctx: Dict[str, Dict[str, Any]] = {}
        self.episodes_file = DATA_DIR / "episodes.jsonl"
        self.semantic_file = DATA_DIR / "semantic.jsonl"
        self.tfidf = TfidfVectorizer(max_features=5000)
        self._fit = False

    # Éphémère
    def load_context(self, user_id: str, session_id: str) -> Dict:
        return self.session_ctx.get(session_id, {})

    # Épisodique
    def store_episode(self, user_id: str, session_id: str, obs: Dict[str, Any]):
        with self.episodes_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"user_id": user_id, "session_id": session_id, **obs}, ensure_ascii=False) + "\n")

    # Sémantique (MVP TF-IDF; upgrade → embeddings + FAISS/Milvus)
    def retrieve_semantic(self, user_id: str, query: str, k: int = 5) -> List[Dict[str, Any]]:
        docs: List[Dict[str, Any]] = []
        if self.semantic_file.exists():
            with self.semantic_file.open("r", encoding="utf-8") as f:
                for line in f:
                    docs.append(json.loads(line))
        if not docs:
            return []
        corpus = [d.get("text", "") for d in docs]
        if not self._fit and corpus:
            self.tfidf.fit(corpus)
            self._fit = True
        dv = self.tfidf.transform(corpus)
        qv = self.tfidf.transform([query])
        sims = (qv @ dv.T).toarray()[0]
        idx = np.argsort(-sims)[:k]
        return [docs[i] | {"score": float(sims[i])} for i in idx]

    def maybe_persist(self, user_id: str, session_id: str, user_msg: str, answer: str, observations: List[Dict[str, Any]]):
        with self.semantic_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"user_id": user_id, "text": user_msg + "\n" + answer}, ensure_ascii=False) + "\n")
