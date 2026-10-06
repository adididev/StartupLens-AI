from sentence_transformers import SentenceTransformer
import numpy as np

# Load model globally so it's only loaded once
model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

def get_embeddings(texts: list[str]) -> np.ndarray:
    """
    Converts a list of text strings into numpy array of embeddings.
    """
    if not texts:
        return np.array([])
        
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings
