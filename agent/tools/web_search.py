# Stub: renvoie des résultats factices.
# Remplacez par une vraie intégration (SerpAPI, Bing, Tavily, etc.).
from typing import List, Dict

def web_search(query: str, top_k: int = 3) -> List[Dict]:
    return [
        {"title": f"Résultat simulé pour: {query}", "url": "https://example.com", "snippet": "Extrait lorem ipsum..."}
        for _ in range(top_k)
    ]
