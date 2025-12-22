import os
from zenml import pipeline
from typing import Dict
from data_pipeline import product_data_pipeline

from src.steps.product_embeddings import generate_product_embeddings
from src.steps.store_embeddings import store_embeddings_pinecone

@pipeline
def product_embedding_pipeline(
        mongodb_uri: str,
        database_name: str,
        pinecone_api_key: str,
        index_name: str,
        nvidia_api_key: str,
        batch_size: int = 100
) -> Dict:
    """Pipeline to generate and store product embeddings in Pinecone"""

    processed_products = product_data_pipeline(mongodb_uri, database_name)
    # Generate embeddings with NVIDIA
    product_embeddings = generate_product_embeddings(
        processed_products,
        nvidia_api_key=nvidia_api_key,
        batch_size=batch_size
    )

    # Store in Pinecone
    storage_stats = store_embeddings_pinecone(
        product_embeddings,
        pinecone_api_key,
        index_name
    )

    return storage_stats


if __name__ == '__main__':

    from dotenv import load_dotenv

    load_dotenv()

    mongodb_uri = os.getenv('mongodb_uri')
    database_name = 'appetit_db'

    pinecone_api_key = os.getenv('PINECONE_API_KEY')
    index_name = "product-embeddings-v2"
    nvidia_api_key = os.getenv('NVIDIA_API_KEY', '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')

    # Run pipeline
    product_embedding_pipeline(
        mongodb_uri,
        database_name,
        pinecone_api_key,
        index_name,
        nvidia_api_key,
        batch_size=100
    )