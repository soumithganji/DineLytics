import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# --- Cached MongoDB client (reused across calls) ---
_mongo_client = None

def _get_db():
    global _mongo_client
    uri = os.getenv("mongodb_uri", "mongodb://localhost:27017")
    db_name = os.getenv("database_name", "appetit_db")
    if _mongo_client is None:
        _mongo_client = MongoClient(uri)
    return _mongo_client[db_name]


def search_db_entities(search_term: str) -> str:
    """
    Search for items or categories in the local MongoDB database.
    Use this if the semantic search fails or doesn't return relevant results.
    
    Args:
        search_term (str): The keyword to search for (e.g., 'pasta', 'pizza').
        
    Returns:
        str: A summary of matching products and categories found in the database.
    """
    try:
        db = _get_db()
        
        results = []
        
        # 1. Search in Categories
        categories = list(db.categories.find({
            "$or": [
                {"name": {"$regex": search_term, "$options": "i"}},
                {"description": {"$regex": search_term, "$options": "i"}}
            ]
        }))
        
        if categories:
            cat_info = [f"Category: {c['name']} (ID: {c['_id']})" for c in categories]
            results.append("Found matching categories:\n" + "\n".join(cat_info))
            
            # For each category, find some products
            for cat in categories:
                prods = list(db.products.find({"category_id": cat["_id"]}).limit(10))
                if prods:
                    prod_names = [p["name"] for p in prods]
                    results.append(f"Products in '{cat['name']}': {', '.join(prod_names)}")

        # 2. Search in Products
        products = list(db.products.find({
            "$or": [
                {"name": {"$regex": search_term, "$options": "i"}},
                {"description": {"$regex": search_term, "$options": "i"}}
            ]
        }).limit(10))
        
        if products:
            prod_info = [f"Product: {p['name']} (ID: {p['_id']})" for p in products]
            results.append("Found matching products:\n" + "\n".join(prod_info))

        if not results:
            return f"No matches found for '{search_term}' in the database."
            
        return "\n\n".join(results)

    except Exception as e:
        return f"Error searching database: {str(e)}"
