import os
import threading

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
_nvidia_key = os.getenv("NVIDIA_API_KEY", "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")
os.environ["NVIDIA_API_KEY"] = _nvidia_key
os.environ["NVIDIA_NIM_API_KEY"] = _nvidia_key
os.environ["NVIDIA_NIM_API_BASE"] = "https://integrate.api.nvidia.com/v1"

from conversation import ConversationBufferWindow
from ui.styles import apply_css
from schema_loader import all_schemas_string
from ui.chat_utils import *
from ui.sidebar import render_sidebar
from ui.chat_interface import create_chat_interface

# Environment variables
mongodb_uri = os.getenv("mongodb_uri")
database_name = os.getenv("database_name")
collection_names = [
    "categories", "delivery_fees", "locations", "merchant_logs",
    "merchant_settings", "orders", "product_categories", "products",
    "stores", "store_tables", "users"
]


# ---------------------------------------------------------------------------
# Background preloading of heavy dependencies (langchain, torch, etc.)
# Starts immediately when the module loads so imports happen while the UI renders.
# ---------------------------------------------------------------------------
_preload_done = threading.Event()

def _preload_heavy_deps():
    """Import heavy packages in background so the first query is fast."""
    try:
        from services.llm import _get_nvidia_llm
        _get_nvidia_llm()                  # pre-warm the LLM client
        # Pre-warm embedding model + Pinecone so first food query is fast
        from services.food_search import _get_embedding_model, _get_pinecone_index
        _get_embedding_model()
        _get_pinecone_index()
        # Pre-warm the PythonREPL
        from services.code_executor import _get_repl
        _get_repl()
        # Pre-import the direct query pipeline
        from query_pipeline import run_data_query  # noqa: F401
    except Exception as e:
        print(f"[preload] warning: {e}")
    finally:
        _preload_done.set()


class ChatbotFlow:
    """Plain-Python query router."""

    def __init__(self):
        self.conversation_history: ConversationBufferWindow = ConversationBufferWindow()
        self.current_query: str = ""
        self.response: str = ""

    # -- alias so chat_interface.py can access flow.state.* unchanged ------
    @property
    def state(self):
        return self

    def clear_progress(self):
        pass

    def kickoff(self):
        """Run the full classify → route → respond pipeline."""
        from services.llm import extract_and_classify_query, _get_nvidia_llm

        print(f"Processing input: {self.current_query}")

        # 1. Classify + enhance
        enhanced_query, is_task = extract_and_classify_query(
            self.conversation_history.get_conversation_string(),
            self.current_query,
        )
        if enhanced_query:
            self.current_query = enhanced_query
            print(f"Enhanced query: {enhanced_query}")

        self.conversation_history.add_message("User", self.current_query)

        # 2. Route
        if is_task:
            self._handle_task_query()
        else:
            self._handle_general_query(_get_nvidia_llm())

        # 3. Store response in memory
        self.conversation_history.add_message("AI", self.response)
        print(f"AI response: {self.response}")

    # -- handlers ----------------------------------------------------------

    def _handle_task_query(self):
        """Direct 2-LLM-call pipeline."""
        from query_pipeline import run_data_query

        self.response = run_data_query(
            user_query=self.current_query,
            schemas=all_schemas_string,
            mongodb_uri=mongodb_uri,
            database_name=database_name,
            collection_names=collection_names,
            conversation_history=self.conversation_history.get_conversation_string(),
        )

    def _handle_general_query(self, llm):
        """Direct LLM call for simple chat."""
        messages = [
            {"role": "system", "content": "You are DineLytics, a friendly AI assistant for a food delivery analytics app. Be concise and helpful."},
            {"role": "user", "content": f"Conversation so far:\n{self.conversation_history.get_conversation_string()}\n\nUser: {self.current_query}"},
        ]
        resp = llm.invoke(messages)
        self.response = resp.content.strip()


# Kick off the background preload
threading.Thread(target=_preload_heavy_deps, daemon=True).start()


def _create_flow():
    """Factory that waits for background preload then creates a flow instance."""
    _preload_done.wait()          # no-op if preload already finished
    return ChatbotFlow()


def main():

    st.set_page_config(page_title="DineLytics", layout="centered", initial_sidebar_state="collapsed")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = load_chat_history()
    if 'current_thread' not in st.session_state:
        st.session_state.current_thread = None
    if 'show_placeholder' not in st.session_state:
        st.session_state.show_placeholder = True

    if 'memory' not in st.session_state:
        st.session_state.memory = ConversationBufferWindow(window_size=10)

    if 'messages_container' not in st.session_state:
        st.session_state.messages_container = None

    with st.sidebar:
        render_sidebar()

    apply_css()

    create_chat_interface(_create_flow, mongodb_uri, database_name, collection_names)

if __name__ == "__main__":
    main()
