from rag.embeddings import get_embeddings
from rag.vector_store import search
import numpy as np

def retrieve(query: str, index, texts: list[str], k: int = 5) -> list[str]:
    """
    Given a query and a FAISS index, retrieves the top-k most relevant chunks.
    """
    if not texts or index is None:
        return []
        
    query_emb = get_embeddings([query])
    if query_emb.size == 0:
        return []
        
    distances, indices = search(index, query_emb, k=k)
    
    retrieved_texts = []
    for idx in indices:
        if idx < len(texts) and idx != -1:
            retrieved_texts.append(texts[idx])
            
    return retrieved_texts
