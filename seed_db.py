import os
import random
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import certifi

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv("mongodb_uri", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("database_name", "appetit_db")


def seed_database():
    print(f"Connecting to MongoDB at {MONGODB_URI}...")
    client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
    db = client[DATABASE_NAME]

    now = datetime.now()

    # ----------------------------
    # 1. Categories
    # ----------------------------
    print("Seeding categories...")
    categories_col = db["categories"]
    categories_col.delete_many({})

    category_list = [
        {"_id": ObjectId(), "name": "Italian", "description": "Authentic Italian pasta and pizzas"},
        {"_id": ObjectId(), "name": "Indian", "description": "Spicy and flavorful Indian curries"},
        {"_id": ObjectId(), "name": "Burgers", "description": "Juicy grilled burgers"},
        {"_id": ObjectId(), "name": "Desserts", "description": "Sweet treats and pastries"},
        {"_id": ObjectId(), "name": "Mexican", "description": "Tacos, burritos, and bold flavors"},
        {"_id": ObjectId(), "name": "Chinese", "description": "Classic stir-fries, noodles, and dim sum"},
        {"_id": ObjectId(), "name": "Japanese", "description": "Sushi, ramen, and Japanese comfort food"},
        {"_id": ObjectId(), "name": "Thai", "description": "Balanced sweet-spicy-sour Thai cuisine"},
        {"_id": ObjectId(), "name": "Mediterranean", "description": "Fresh bowls, kebabs, and mezze"},
        {"_id": ObjectId(), "name": "Seafood", "description": "Fresh fish, shrimp, and coastal classics"},
        {"_id": ObjectId(), "name": "Breakfast", "description": "Morning favorites, eggs, and pancakes"},
        {"_id": ObjectId(), "name": "Healthy", "description": "Salads, bowls, and lighter options"},
        {"_id": ObjectId(), "name": "Pizza", "description": "From classic pies to specialty pizzas"},
        {"_id": ObjectId(), "name": "Vegan", "description": "Plant-based meals and desserts"},
        {"_id": ObjectId(), "name": "Coffee", "description": "Coffee, espresso drinks, and pastries"},
    ]
    categories_col.insert_many(category_list)

    # Helper: name -> id
    cat_id = {c["name"]: c["_id"] for c in category_list}

    # ----------------------------
    # 2. Stores
    # ----------------------------
    print("Seeding stores...")
    stores_col = db["stores"]
    stores_col.delete_many({})

    store_list = [
        {"_id": ObjectId(), "name": "Little Italy", "location": "Buffalo Downtown", "rating": 4.5},
        {"_id": ObjectId(), "name": "Spice Route", "location": "Amherst", "rating": 4.8},
        {"_id": ObjectId(), "name": "Burger Joint", "location": "Niagara", "rating": 4.2},

        {"_id": ObjectId(), "name": "Taco Fiesta", "location": "Buffalo West Side", "rating": 4.6},
        {"_id": ObjectId(), "name": "Dragon Wok", "location": "Cheektowaga", "rating": 4.4},
        {"_id": ObjectId(), "name": "Sakura Sushi", "location": "Williamsville", "rating": 4.7},
        {"_id": ObjectId(), "name": "Bangkok Bites", "location": "Buffalo Elmwood", "rating": 4.6},
        {"_id": ObjectId(), "name": "Mediterraneo Grill", "location": "Kenmore", "rating": 4.5},
        {"_id": ObjectId(), "name": "Harbor Catch", "location": "Buffalo Canalside", "rating": 4.3},
        {"_id": ObjectId(), "name": "Sunrise Diner", "location": "Tonawanda", "rating": 4.1},
        {"_id": ObjectId(), "name": "Green Bowl Co.", "location": "Buffalo North Buffalo", "rating": 4.4},
        {"_id": ObjectId(), "name": "Slice Society", "location": "Buffalo Allentown", "rating": 4.5},
        {"_id": ObjectId(), "name": "Vegan Vibes", "location": "Buffalo Hertel", "rating": 4.6},
        {"_id": ObjectId(), "name": "Bean & Butter", "location": "Buffalo Downtown", "rating": 4.7},
    ]
    stores_col.insert_many(store_list)

    store_id = {s["name"]: s["_id"] for s in store_list}

    # ----------------------------
    # 3. Products
    # ----------------------------
    print("Seeding products...")
    products_col = db["products"]
    products_col.delete_many({})

    def make_product(name, desc, price, store_name, category_name, active=True, created_at=None):
        return {
            "_id": ObjectId(),
            "name": name,
            "description": desc,
            "price": float(price),
            "store": store_id[store_name],
            "category_id": cat_id[category_name],
            "is_active": active,
            "createdAt": created_at or now - timedelta(days=random.randint(0, 45)),
        }

    products = []

    # Little Italy (Italian + Pizza + Desserts)
    products += [
        make_product("Margherita Pizza", "Classic tomato, basil and mozzarella", 12.0, "Little Italy", "Pizza"),
        make_product("Pepperoni Pizza", "Pepperoni, mozzarella, house sauce", 14.0, "Little Italy", "Pizza"),
        make_product("Fettuccine Alfredo", "Creamy pasta with parmesan", 15.0, "Little Italy", "Italian"),
        make_product("Spaghetti Bolognese", "Slow-simmered meat sauce", 16.0, "Little Italy", "Italian"),
        make_product("Pasta Primavera", "Fresh seasonal vegetables with pasta", 14.0, "Little Italy", "Italian"),
        make_product("Pasta Carbonara", "Creamy bacon and egg pasta", 15.5, "Little Italy", "Italian"),
        make_product("Tiramisu", "Espresso-soaked ladyfingers and mascarpone", 7.5, "Little Italy", "Desserts"),
    ]

    # Spice Route (Indian)
    products += [
        make_product("Chicken Biryani", "Fragrant rice with spiced chicken", 14.0, "Spice Route", "Indian"),
        make_product("Butter Chicken", "Mild creamy tomato curry", 16.0, "Spice Route", "Indian"),
        make_product("Chana Masala", "Chickpeas in a spiced tomato gravy", 13.0, "Spice Route", "Indian"),
        make_product("Garlic Naan", "Soft naan brushed with garlic butter", 3.5, "Spice Route", "Indian"),
        make_product("Mango Lassi", "Sweet mango yogurt drink", 4.5, "Spice Route", "Indian"),
    ]

    # Burger Joint (Burgers + Desserts + Breakfast)
    products += [
        make_product("Classic Cheeseburger", "Beef patty with cheddar", 10.0, "Burger Joint", "Burgers"),
        make_product("Bacon BBQ Burger", "Bacon, BBQ sauce, crispy onions", 12.5, "Burger Joint", "Burgers"),
        make_product("Crispy Chicken Sandwich", "Fried chicken, pickles, mayo", 11.0, "Burger Joint", "Burgers"),
        make_product("Fries", "Golden crispy fries", 3.5, "Burger Joint", "Burgers"),
        make_product("Milkshake", "Vanilla / chocolate / strawberry", 5.5, "Burger Joint", "Desserts"),
        make_product("Breakfast Burger", "Egg, cheese, and bacon on a bun", 12.0, "Burger Joint", "Breakfast"),
    ]

    # Taco Fiesta (Mexican)
    products += [
        make_product("Carne Asada Tacos", "Steak, onion, cilantro, salsa", 11.0, "Taco Fiesta", "Mexican"),
        make_product("Chicken Quesadilla", "Grilled chicken, cheese, pico", 12.0, "Taco Fiesta", "Mexican"),
        make_product("Veggie Burrito", "Rice, beans, fajita veg, guac", 12.5, "Taco Fiesta", "Mexican"),
        make_product("Chips & Guacamole", "Fresh guac with tortilla chips", 7.0, "Taco Fiesta", "Mexican"),
        make_product("Churros", "Cinnamon sugar churros with dip", 6.0, "Taco Fiesta", "Desserts"),
    ]

    # Dragon Wok (Chinese)
    products += [
        make_product("General Tso's Chicken", "Sweet-spicy crispy chicken", 14.0, "Dragon Wok", "Chinese"),
        make_product("Beef & Broccoli", "Tender beef in savory sauce", 15.0, "Dragon Wok", "Chinese"),
        make_product("Vegetable Lo Mein", "Noodles tossed with mixed veg", 13.0, "Dragon Wok", "Chinese"),
        make_product("Fried Rice", "Egg fried rice with scallions", 11.0, "Dragon Wok", "Chinese"),
        make_product("Dumplings", "Pork or veggie dumplings", 8.0, "Dragon Wok", "Chinese"),
    ]

    # Sakura Sushi (Japanese)
    products += [
        make_product("Spicy Tuna Roll", "Tuna, spicy mayo, cucumber", 9.5, "Sakura Sushi", "Japanese"),
        make_product("Salmon Avocado Roll", "Salmon with avocado", 10.0, "Sakura Sushi", "Japanese"),
        make_product("Chicken Ramen", "Rich broth, noodles, chicken", 15.0, "Sakura Sushi", "Japanese"),
        make_product("Miso Soup", "Classic miso with tofu and scallion", 3.0, "Sakura Sushi", "Japanese"),
        make_product("Sashimi Sampler", "Chef selection of fresh sashimi", 18.0, "Sakura Sushi", "Seafood"),
    ]

    # Bangkok Bites (Thai)
    products += [
        make_product("Pad Thai", "Rice noodles, tamarind, peanuts", 14.0, "Bangkok Bites", "Thai"),
        make_product("Green Curry", "Coconut curry with basil", 15.5, "Bangkok Bites", "Thai"),
        make_product("Tom Yum Soup", "Hot & sour soup with shrimp", 13.0, "Bangkok Bites", "Thai"),
        make_product("Thai Iced Tea", "Sweet creamy Thai tea", 4.0, "Bangkok Bites", "Thai"),
    ]

    # Mediterraneo Grill (Mediterranean)
    products += [
        make_product("Chicken Shawarma Plate", "Chicken, rice, salad, garlic sauce", 16.0, "Mediterraneo Grill", "Mediterranean"),
        make_product("Falafel Wrap", "Crispy falafel with tahini", 12.0, "Mediterraneo Grill", "Mediterranean"),
        make_product("Hummus & Pita", "Creamy hummus with warm pita", 8.0, "Mediterraneo Grill", "Mediterranean"),
        make_product("Greek Salad", "Feta, olives, cucumber, tomato", 11.5, "Mediterraneo Grill", "Healthy"),
    ]

    # Harbor Catch (Seafood)
    products += [
        make_product("Fish & Chips", "Beer-battered cod with fries", 17.0, "Harbor Catch", "Seafood"),
        make_product("Shrimp Po' Boy", "Crispy shrimp, lettuce, remoulade", 16.0, "Harbor Catch", "Seafood"),
        make_product("Lobster Roll", "Chilled lobster with buttered roll", 24.0, "Harbor Catch", "Seafood"),
        make_product("Clam Chowder", "Creamy chowder with clams", 8.5, "Harbor Catch", "Seafood"),
    ]

    # Sunrise Diner (Breakfast + Desserts)
    products += [
        make_product("Pancake Stack", "Three pancakes with syrup", 10.0, "Sunrise Diner", "Breakfast"),
        make_product("Classic Omelette", "3-egg omelette with cheese", 11.5, "Sunrise Diner", "Breakfast"),
        make_product("Breakfast Burrito", "Eggs, potatoes, cheese, salsa", 12.0, "Sunrise Diner", "Breakfast"),
        make_product("French Toast", "Brioche french toast, powdered sugar", 11.0, "Sunrise Diner", "Breakfast"),
        make_product("Apple Pie", "Warm apple pie slice", 6.5, "Sunrise Diner", "Desserts"),
    ]

    # Green Bowl Co. (Healthy)
    products += [
        make_product("Chicken Caesar Salad", "Romaine, parmesan, croutons", 13.0, "Green Bowl Co.", "Healthy"),
        make_product("Quinoa Power Bowl", "Quinoa, chickpeas, veg, tahini", 14.0, "Green Bowl Co.", "Healthy"),
        make_product("Avocado Toast", "Sourdough, avocado, chili flakes", 9.5, "Green Bowl Co.", "Breakfast"),
        make_product("Berry Smoothie", "Mixed berries, yogurt, honey", 7.0, "Green Bowl Co.", "Healthy"),
    ]

    # Slice Society (Pizza)
    products += [
        make_product("NY Style Cheese Slice", "Big foldable slice", 4.0, "Slice Society", "Pizza"),
        make_product("Sausage & Peppers Pizza", "Italian sausage, peppers, onions", 16.0, "Slice Society", "Pizza"),
        make_product("White Pizza", "Ricotta, mozzarella, garlic", 15.0, "Slice Society", "Pizza"),
        make_product("Cannoli", "Ricotta cream filled pastry", 6.0, "Slice Society", "Desserts"),
    ]

    # Vegan Vibes (Vegan + Desserts)
    products += [
        make_product("Vegan Burger", "Plant-based patty, vegan cheese", 13.5, "Vegan Vibes", "Vegan"),
        make_product("Tofu Stir-Fry", "Crispy tofu, veggies, ginger sauce", 14.0, "Vegan Vibes", "Vegan"),
        make_product("Vegan Mac & Cheese", "Creamy cashew-based sauce", 13.0, "Vegan Vibes", "Vegan"),
        make_product("Vegan Brownie", "Fudgy chocolate brownie", 5.5, "Vegan Vibes", "Desserts"),
    ]

    # Bean & Butter (Coffee + Breakfast + Desserts)
    products += [
        make_product("Latte", "Espresso with steamed milk", 4.75, "Bean & Butter", "Coffee"),
        make_product("Cold Brew", "Smooth slow-steeped coffee", 4.5, "Bean & Butter", "Coffee"),
        make_product("Cappuccino", "Espresso with foamed milk", 4.5, "Bean & Butter", "Coffee"),
        make_product("Butter Croissant", "Flaky buttery pastry", 4.0, "Bean & Butter", "Desserts"),
        make_product("Breakfast Sandwich", "Egg, cheese, choice of bacon/sausage", 7.5, "Bean & Butter", "Breakfast"),
    ]

    # Optional: randomly deactivate a few products for realism
    for p in random.sample(products, k=min(6, len(products))):
        p["is_active"] = random.choice([True, True, True, False])

    products_col.insert_many(products)

    # ----------------------------
    # 4. Users
    # ----------------------------
    print("Seeding users...")
    users_col = db["users"]
    users_col.delete_many({})

    first_names = [
        "John", "Jane", "Ava", "Noah", "Sophia", "Liam", "Mia", "Ethan", "Isabella",
        "Lucas", "Amelia", "Benjamin", "Charlotte", "Henry", "Evelyn", "Daniel",
        "Harper", "Matthew", "Emily", "James", "Olivia", "Alexander", "Ella",
        "Michael", "Abigail", "William", "Madison", "Joseph", "Scarlett",
        "David", "Victoria", "Samuel", "Grace", "Andrew", "Chloe", "Joshua",
        "Lily", "Ryan", "Zoey", "Nathan", "Hannah", "Christian", "Aria",
        "Jonathan", "Penelope", "Logan", "Riley", "Justin", "Nora"
    ]

    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
    ]

    user_list = []
    used_emails = set()

    for i in range(100):
        first = random.choice(first_names)
        last = random.choice(last_names)
        name = f"{first} {last}"

        email = f"{first.lower()}.{last.lower()}{i}@example.com"
        phone = f"+1-716-555-{str(1000 + i).zfill(4)}"

        user_list.append({
            "_id": ObjectId(),
            "name": name,
            "email": email,
            "phone": phone,
            "createdAt": datetime.now() - timedelta(days=random.randint(0, 365)),
            "is_active": random.choice([True, True, True, False])  # mostly active
        })

    users_col.insert_many(user_list)

    # ----------------------------
    # 5. Orders
    # ----------------------------
    print("Seeding orders...")
    orders_col = db["orders"]
    orders_col.delete_many({})

    # Build helper map: store_id -> products list
    products_by_store = {}
    for p in products:
        products_by_store.setdefault(p["store"], []).append(p)

    statuses = ["completed", "completed", "completed", "cancelled", "refunded"]
    delivery_statuses = ["delivered", "delivered", "delivered", "failed", "returned"]

    orders = []
    for _ in range(1000):  # more orders
        user = random.choice(user_list)
        store = random.choice(store_list)

        store_products = [p for p in products_by_store.get(store["_id"], []) if p.get("is_active", True)]
        if not store_products:
            continue

        # 1-4 line items
        line_count = random.randint(1, 4)
        chosen = random.sample(store_products, k=min(line_count, len(store_products)))

        details = []
        subtotal = 0.0
        for prod in chosen:
            qty = random.randint(1, 3)
            line_total = float(prod["price"]) * qty
            subtotal += line_total
            details.append(
                {
                    "product_id": prod["_id"],
                    "name": prod["name"],
                    "qty": qty,
                    "price": float(prod["price"]),
                    "total_amount": line_total,
                }
            )

        delivery_fee = random.choice([2.99, 3.99, 4.99, 5.99, 6.99])
        tax = round(subtotal * 0.08, 2)  # simple 8% tax assumption
        tip = random.choice([0.0, 2.0, 3.0, 5.0, 7.0])

        order_date = now - timedelta(days=random.randint(0, 60), hours=random.randint(0, 23))
        status = random.choice(statuses)
        delivery_status = random.choice(delivery_statuses) if status != "completed" else "delivered"

        orders.append(
            {
                "_id": ObjectId(),
                "createdAt": order_date,
                "store_id": store["_id"],
                "user_id": user["_id"],
                "status": status,
                "delivery_status": delivery_status,
                "subtotal": round(subtotal, 2),
                "delivery_fee": delivery_fee,
                "tax": tax,
                "tip": tip,
                "total_amount": round(subtotal + delivery_fee + tax + tip, 2),
                "details": details,
            }
        )

    if orders:
        orders_col.insert_many(orders)

    # ----------------------------
    # 6-11. Other collections (placeholders)
    # ----------------------------
    for col_name in [
        "delivery_fees",
        "locations",
        "merchant_logs",
        "merchant_settings",
        "product_categories",
        "store_tables",
    ]:
        print(f"Seeding {col_name}...")
        db[col_name].delete_many({})
        db[col_name].insert_one({"info": f"Sample data for {col_name}", "createdAt": now})

    print("\nDatabase seeded successfully!")
    print(f"Total Categories: {categories_col.count_documents({})}")
    print(f"Total Stores: {stores_col.count_documents({})}")
    print(f"Total Products: {products_col.count_documents({})}")
    print(f"Total Users: {users_col.count_documents({})}")
    print(f"Total Orders: {orders_col.count_documents({})}")


if __name__ == "__main__":
    seed_database()