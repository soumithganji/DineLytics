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


def filter_items(food_item_name: str) -> str:
    """
    Find food names semantically equivalent to the food name in user query

    Args:
        food_item_name (str): food name from user query.

    Returns:
        str: string containing food names semantically equivalent to provided item_name.
    """

    try:
        model = _get_embedding_model()
        index = _get_pinecone_index()

        item_embedding = model.encode(food_item_name, convert_to_tensor=True).cpu().numpy().tolist()

        query_response = index.query(
            vector=item_embedding,
            top_k=10,
            include_metadata=True
        )

        equivalent_items = []
        for match in query_response['matches']:
            equivalent_items.append(match['metadata']['food_item'])

        if not equivalent_items:
            return "No semantically equivalent food items found."

        return ", ".join(set(equivalent_items))

    except Exception as e:
        return f"Error in Food Items Finder: {str(e)}"

# Test code (commented out)
if __name__ == "__main__":
    from time import time

    start = time()
    test_item = "Mac and Cheese"
    food_items_finder = filter_items
    result = food_items_finder(test_item)
    print(f"Semantically equivalent food items to '{test_item}':")
    print(result)
    end = time()

    print(end - start)