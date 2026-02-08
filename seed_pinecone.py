"""
Populate Pinecone 'food' index with product names from MongoDB.
Run this once to seed the vector database for semantic food search.
"""

import os
from dotenv import load_dotenv
load_dotenv()

import certifi
from pymongo import MongoClient
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import torch

def seed_pinecone():
    print("Connecting to MongoDB...")
    client = MongoClient(os.getenv('mongodb_uri'), tlsCAFile=certifi.where())
    db = client[os.getenv('database_name')]
    
    # Get all unique product names
    print("Fetching products from MongoDB...")
    products = list(db.products.find({}, {'name': 1, '_id': 0}))
    food_names = list(set(p['name'] for p in products))
    print(f"Found {len(food_names)} unique products")
    
    # Also get food names from order details (in case of variations)
    print("Fetching food names from orders...")
    pipeline = [
        {'$unwind': '$details'},
        {'$group': {'_id': '$details.name'}},
    ]
    order_foods = [doc['_id'] for doc in db.orders.aggregate(pipeline)]
    food_names = list(set(food_names + order_foods))
    print(f"Total unique food items: {len(food_names)}")
    
    client.close()
    
    # Load embedding model
    print("Loading embedding model...")
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2').to(device)
    
    # Generate embeddings
    print("Generating embeddings...")
    embeddings = model.encode(food_names, convert_to_tensor=True, show_progress_bar=True)
    embeddings = embeddings.cpu().numpy()
    
    # Connect to Pinecone
    print("Connecting to Pinecone...")
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    index = pc.Index("food")
    
    # Prepare vectors for upsert
    vectors = []
    for i, (name, embedding) in enumerate(zip(food_names, embeddings)):
        vectors.append({
            'id': f'food_{i}',
            'values': embedding.tolist(),
            'metadata': {'food_item': name}
        })
    
    # Upsert in batches of 100
    print("Upserting to Pinecone...")
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)
        print(f"  Upserted {min(i + batch_size, len(vectors))}/{len(vectors)}")
    
    # Verify
    stats = index.describe_index_stats()
    print(f"\n✅ Pinecone index populated!")
    print(f"   Total vectors: {stats.total_vector_count}")

if __name__ == "__main__":
    seed_pinecone()
