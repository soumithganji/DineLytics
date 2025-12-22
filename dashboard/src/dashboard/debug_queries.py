#!/usr/bin/env python
"""Debug script to verify MongoDB pizza/burger data for November 2025."""
import os
import sys
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("mongodb_uri", "mongodb://localhost:27017")
db_name = os.getenv("database_name", "appetit_db")

client = MongoClient(uri, serverSelectionTimeoutMS=10000)
db = client[db_name]

nov_start = datetime(2025, 11, 1)
dec_start = datetime(2025, 12, 1)

# Pizza sales in November
pipeline = [
    {"$match": {"createdAt": {"$gte": nov_start, "$lt": dec_start}}},
    {"$unwind": "$details"},
    {"$match": {"details.name": {"$regex": "pizza", "$options": "i"}}},
    {"$group": {
        "_id": "$details.name",
        "count": {"$sum": "$details.qty"},
        "total": {"$sum": "$details.total_amount"}
    }},
    {"$sort": {"total": -1}}
]

results = list(db.orders.aggregate(pipeline))
print("Pizza sales in November 2025:")
for r in results:
    print(f"  {r['_id']}: {r['count']} items, ${r['total']:.2f}")

if not results:
    print("  No pizza orders found")

# Burger sales in November
pipeline[2] = {"$match": {"details.name": {"$regex": "burger", "$options": "i"}}}
results = list(db.orders.aggregate(pipeline))
print("\nBurger sales in November 2025:")
for r in results:
    print(f"  {r['_id']}: {r['count']} items, ${r['total']:.2f}")

if not results:
    print("  No burger orders found")

