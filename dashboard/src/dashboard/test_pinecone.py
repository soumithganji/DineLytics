import os
import torch
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

def test_items_finder(query):
    print(f"Testing Items Finder for: {query}")
    try:
        pinecone_key = os.getenv('PINECONE_API_KEY')
        pc = Pinecone(api_key=pinecone_key)
        index_name = "food"
        index = pc.Index(index_name)

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2').to(device)

        item_embedding = model.encode(query, convert_to_tensor=True).cpu().numpy().tolist()

        query_response = index.query(
            vector=item_embedding,
            top_k=20,
            include_metadata=True
        )

        equivalent_items = []
        for match in query_response['matches']:
            equivalent_items.append(match['metadata']['food_item'])

        results = list(set(equivalent_items))
        print(f"Results: {results}")
        return results
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    test_items_finder("pasta")
    test_items_finder("pepperoni pizza")
