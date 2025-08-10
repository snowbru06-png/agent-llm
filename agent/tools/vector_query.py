from typing import List, Dict, Any

# NOTE: pour un vrai RAG, remplacez par embeddings + FAISS/Milvus
def vector_query(query: str, k: int = 5) -> List[Dict[str, Any]]:
    return [{"text": f"(MVP) Pas d'index global. Query: {query}", "score": 0.0}]
