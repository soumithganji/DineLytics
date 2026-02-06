"""
Direct query pipeline — lightweight 2-LLM-call approach.

  1. (optional) Food-item lookup via Pinecone  — no LLM needed
  2. LLM call #1: generate pymongo code          — ~3-4s
  3. Execute code locally                         — <1s
  4. LLM call #2: format results for the user     — ~2-3s

Total: 2 LLM calls (~6-8s).
"""

import os
import re
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Simple heuristic: does the query mention a specific food item?
# We look for common food keywords that would benefit from semantic search.
_FOOD_KEYWORDS = re.compile(
    r'\b(pizza|burger|pasta|sandwich|salad|taco|sushi|wings?|fries|'
    r'chicken|steak|soup|wrap|bowl|noodle|rice|curry|bbq|barbecue|'
    r'seafood|shrimp|lobster|crab|fish|pork|beef|lamb|vegan|'
    r'dessert|cake|cookie|pie|brownie|ice\s*cream|donut|doughnut|'
    r'coffee|tea|smoothie|juice|latte|espresso|drink|beverage|'
    r'breakfast|lunch|dinner|brunch|appetizer|entree|mac\s*(and|&|n)\s*cheese)\b',
    re.IGNORECASE
)


def _extract_food_items(query: str) -> list[str]:
    """Return list of food keywords found in the user query."""
    return list({m.group(0).lower() for m in _FOOD_KEYWORDS.finditer(query)})


def _lookup_food_names_pinecone(food_items: list[str]) -> list[str]:
    """Call Food Items Finder (Pinecone) directly — no LLM overhead."""
    if not food_items:
        return []
    try:
        from services.food_search import _get_embedding_model, _get_pinecone_index
        model = _get_embedding_model()
        index = _get_pinecone_index()

        all_names = []
        for item in food_items:
            emb = model.encode(item, convert_to_tensor=True).cpu().numpy().tolist()
            resp = index.query(vector=emb, top_k=10, include_metadata=True)
            names = [m['metadata']['food_item'] for m in resp.get('matches', [])]
            all_names.extend(names)

        return sorted(set(all_names))
    except Exception as e:
        print(f"[direct_pipeline] Pinecone lookup error: {e}")
    return []


def _lookup_food_names_db(food_items: list[str]) -> list[str]:
    """Fallback: search MongoDB products & order details for matching names."""
    if not food_items:
        return []
    try:
        from pymongo import MongoClient
        client = MongoClient(os.getenv('mongodb_uri'))
        db = client[os.getenv('database_name')]

        all_names = set()
        for item in food_items:
            # Search in products collection
            products = db.products.find(
                {'name': {'$regex': item, '$options': 'i'}},
                {'name': 1, '_id': 0}
            )
            for p in products:
                all_names.add(p['name'])

            # Also search in order details for names that exist in real orders
            pipeline = [
                {'$unwind': '$details'},
                {'$match': {'details.name': {'$regex': item, '$options': 'i'}}},
                {'$group': {'_id': '$details.name'}},
                {'$limit': 20}
            ]
            for doc in db.orders.aggregate(pipeline):
                all_names.add(doc['_id'])

        client.close()
        return sorted(all_names)
    except Exception as e:
        print(f"[direct_pipeline] DB food lookup error: {e}")
    return []


def _lookup_food_names(food_items: list[str]) -> str:
    """Try Pinecone first, fall back to direct MongoDB search."""
    if not food_items:
        return ""

    names = _lookup_food_names_pinecone(food_items)
    if not names:
        names = _lookup_food_names_db(food_items)

    if names:
        return f"\nFood name variations found in database: {', '.join(names)}\n"
    return ""


def _extract_code_block(text: str) -> str:
    """Pull the first ```python ... ``` block from LLM output; fallback to full text."""
    m = re.search(r'```(?:python)?\s*\n(.*?)```', text, re.DOTALL)
    if m:
        return m.group(1).strip()
    # Maybe the LLM returned raw code without fences
    if 'import ' in text or 'MongoClient' in text:
        return text.strip()
    return text.strip()


def _execute_code(code: str) -> str:
    """Run code in the cached PythonREPL."""
    from services.code_executor import _get_repl
    try:
        repl = _get_repl()
        result = repl.run(code)
        return result.strip()
    except Exception as e:
        return f"EXECUTION ERROR: {e}"


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_data_query(user_query: str, schemas: str, mongodb_uri: str,
                   database_name: str, collection_names: list,
                   conversation_history: str = "") -> str:
    """
    End-to-end data query in exactly 2 LLM calls.
    Returns the formatted answer string.
    """
    from services.llm import _get_nvidia_llm
    llm = _get_nvidia_llm()
    current_date = datetime.now().strftime("%Y-%m-%d")

    # ── Step 1: food-item lookup (no LLM, just Pinecone) ─────────────
    food_items = _extract_food_items(user_query)
    food_context = _lookup_food_names(food_items)

    # ── Step 2: LLM call #1 — generate pymongo code ──────────────────
    code_prompt = f"""Generate Python/pymongo code for this query. Return ONLY a python code block.

Query: "{user_query}"
Today: {current_date}
MongoDB URI env var: mongodb_uri   Database env var: database_name
Collections: {collection_names}
{food_context}
DATABASE SCHEMAS:
{schemas}

RULES:
- Connect: MongoClient(os.getenv('mongodb_uri')), db = client[os.getenv('database_name')]
- orders.details[] is an array — use $unwind. details[].name=item, details[].price=unit price, details[].qty=quantity, details[].total_amount=item total
- orders.total_amount = entire order total
- Case-insensitive regex ($options:'i') for ALL name filters
- IMPORTANT: When matching food item names, use a CONTAINS regex (no ^ or $ anchors). Product names often include extra words (e.g. "Pepperoni Pizza" not just "Pizza"). Use {{"$regex": "pizza", "$options": "i"}} NOT {{"$regex": "^pizza$"}}{f'''
- For food items, use $regex with alternation for these exact names from the database: {food_context.strip()}. Example: {{"$regex": "name1|name2|name3", "$options": "i"}}''' if food_context else ''}
- Date handling: no time period mentioned = NO date filter. "last month" = prev calendar month. "this month" = current month. "today" = today only.
- Output: print(json.dumps(results, default=str))

Return ONLY the Python code inside ```python ... ``` fences. No explanation."""

    code_response = llm.invoke([
        {"role": "system", "content": "You are a MongoDB/Python expert. Return only executable Python code."},
        {"role": "user", "content": code_prompt}
    ])

    code = _extract_code_block(code_response.content)
    print(f"[direct_pipeline] Generated code:\n{code[:200]}...")

    # ── Step 3: Execute code (no LLM needed) ──────────────────────────
    raw_output = _execute_code(code)
    print(f"[direct_pipeline] Execution output: {raw_output[:300]}...")

    # If execution failed, try one fix
    if "ERROR" in raw_output or "Traceback" in raw_output or "Error" in raw_output[:30]:
        fix_prompt = f"""The code below produced an error. Fix it and return ONLY the corrected python code block.

Code:
```python
{code}
```

Error: {raw_output[:500]}

Return ONLY the fixed Python code inside ```python ... ``` fences."""
        fix_response = llm.invoke([
            {"role": "system", "content": "Fix the Python code. Return only executable code."},
            {"role": "user", "content": fix_prompt}
        ])
        code = _extract_code_block(fix_response.content)
        raw_output = _execute_code(code)
        print(f"[direct_pipeline] Retry output: {raw_output[:300]}...")

    # ── Step 4: LLM call #2 — format results ─────────────────────────
    format_prompt = f"""Format this data as a direct answer to: "{user_query}"

Raw data: {raw_output[:3000]}

Rules:
- Multiple rows → Markdown table (blank line before, each row on new line)
- Single metric → concise sentence (e.g. "Total revenue is $12,345.00")
- No data/empty → polite explanation
- Format financial values with "$" (e.g. $1,234.50)
- Month numbers → names, week numbers → date ranges
- Use human-readable names, not IDs
- ONLY answer what was asked. No technical details about queries.
- Do NOT use a table for single-value answers."""

    format_response = llm.invoke([
        {"role": "system", "content": "You are a data analyst. Present results clearly and concisely."},
        {"role": "user", "content": format_prompt}
    ])

    return format_response.content.strip()
