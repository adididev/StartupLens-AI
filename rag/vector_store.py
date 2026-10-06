import faiss
import numpy as np

def create_index(embeddings: np.ndarray):
    """
    Creates a FAISS index and adds embeddings to it.
    Returns the index.
    """
    if embeddings.size == 0:
        return None
        
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    
    # FAISS requires float32
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    return index

def search(index, query_embedding: np.ndarray, k: int = 5):
    """
    Searches the FAISS index for top-k closest embeddings.
    Returns distances and indices of the top-k results.
    """
    if index is None or query_embedding.size == 0:
        return [], []
        
    query_embedding = query_embedding.astype('float32')
    # Reshape if 1D array
    if len(query_embedding.shape) == 1:
        query_embedding = query_embedding.reshape(1, -1)
        
    faiss.normalize_L2(query_embedding)
    distances, indices = index.search(query_embedding, k)
    
    return distances[0], indices[0]
