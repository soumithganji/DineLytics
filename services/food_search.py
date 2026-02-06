import os

from dotenv import load_dotenv

load_dotenv()

# --- Cached resources (loaded once, reused across calls) ---
_embedding_model = None
_pinecone_index = None

def _get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        import torch
        from sentence_transformers import SentenceTransformer
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        _embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2').to(device)
    return _embedding_model

def _get_pinecone_index():
    global _pinecone_index
    if _pinecone_index is None:
        from pinecone import Pinecone
        pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        _pinecone_index = pc.Index("food")
    return _pinecone_index


