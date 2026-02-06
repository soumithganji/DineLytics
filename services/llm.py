import os
from dotenv import load_dotenv

load_dotenv()
os.environ["NVIDIA_API_KEY"] = os.getenv("NVIDIA_API_KEY", "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")

_nvidia_llm = None

def _get_nvidia_llm():
    global _nvidia_llm
    if _nvidia_llm is None:
        from langchain_nvidia_ai_endpoints import ChatNVIDIA
        _nvidia_llm = ChatNVIDIA(model='meta/llama-3.3-70b-instruct', temperature=0.2)
    return _nvidia_llm

import re

# Fast regex patterns for obvious general conversation (no LLM needed)
_GENERAL_PATTERNS = re.compile(
    r'^\s*('
    r'h(i|ello|ey|owdy|ola)'
    r'|thanks?( you)?|thx|ty'
    r'|bye|goodbye|see ya|later'
    r'|good (morning|afternoon|evening|night)'
    r'|what(s|\s*is)? up'
    r'|how are you'
    r'|ok(ay)?|sure|great|cool|nice|awesome'
    r'|yes|no|nope|yep|yeah'
    r'|who are you|what are you|what can you do'
    r'|help'
    r')\s*[?!.]*\s*$',
    re.IGNORECASE
)


def extract_and_classify_query(conversation_history, user_query):
    """
    Classify + enhance user query. Uses fast regex for obvious greetings,
    falls back to a single LLM call for ambiguous queries.
    Returns (enhanced_query_or_None, is_task_specific).
    """
    # Fast path: obvious greetings / chitchat — skip LLM entirely
    if _GENERAL_PATTERNS.match(user_query):
        return None, False

    prompt = f"""You are a classifier for DineLytics (food delivery analytics).

Conversation: {conversation_history}
Query: "{user_query}"

1. CLASSIFY as "task" (data/analytics: orders, sales, revenue, products, stores, metrics, trends) or "general" (greetings, chitchat).
2. If task: refine query using conversation context (resolve pronouns, add missing context). Keep time-unspecified queries as-is ("till now" = all data). If general: enhanced_query=null.

Return ONLY JSON: {{"classification":"task"|"general","enhanced_query":"..."|null}}"""

    try:
        messages = [
            {"role": "system", "content": "Return only valid JSON."},
            {"role": "user", "content": prompt}
        ]
        response = _get_nvidia_llm().invoke(messages)
        import json as _json
        result = _json.loads(response.content.strip())
        is_task = result.get("classification", "general").lower() == "task"
        enhanced = result.get("enhanced_query")
        return enhanced, is_task
    except Exception as e:
        print(f"Error in extract_and_classify_query: {str(e)}")
        return user_query, True