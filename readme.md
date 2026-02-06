# DineLytics — Advanced Analytics Chatbot

DineLytics is a production-grade AI analytics assistant designed to democratize access to business data. It allows users to ask complex questions about restaurant operations, sales, and inventory in plain English and receive precise, tabular insights, bypassing the need for database knowledge or complex BI tools.

🔗 **Try the Live Demo Here: [DineLytics](https://dinelytics-650060583648.us-central1.run.app)**

![DineLytics Preview](assets/dinelytics_preview.png)

##  Key Features

*   **Direct Query Pipeline**: A lightweight LLM pipeline that generates pymongo code and formats results — fast and deterministic.
*   **Semantic Understanding**: Uses **NVIDIA Embeddings** and **Pinecone** to resolve naming inconsistencies (e.g., matching "Mac n Cheese" to "Mac & Cheese") via semantic search.
*   **Conversational Memory**: Maintains context across the session to support follow-up questions.
*   **Schema-Aware**: Dynamically adapts to your specific MongoDB schema structure.

##  Tech Stack

*   **Language**: Python 3.12+
*   **Frameworks & Libraries**:
    *   **LangChain**: Tooling and LLM abstraction.
    *   **Streamlit**: Interactive web interface.
    *   **Pydantic**: Data validation and detailed schema definitions.
    *   **PyMongo**: Direct database interaction.
*   **AI & Data**:
    *   **LLMs**: NVIDIA NIM (Llama 3.3).
    *   **Vector DB**: Pinecone (for semantic item lookup).
    *   **Database**: MongoDB.
*   **Infrastructure**:
    *   **Docker & Docker Compose**: Containerization and orchestration.

##  Project Structure

```text
DineLytics/
├── app.py                   # Main entry point and query routing
├── conversation.py          # Conversation memory management
├── query_pipeline.py        # Direct 2-LLM-call data query pipeline
├── schema_loader.py         # Schema config loading and formatting
├── seed_db.py               # Standalone DB seeding script
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── schemas/                 # JSON schemas + schema.yaml mapping
├── services/                # Backend services
│   ├── llm.py               # NVIDIA LLM client + query classifier
│   ├── food_search.py       # Pinecone semantic food item lookup
│   └── code_executor.py     # Python REPL for generated code
├── ui/                      # Streamlit UI layer
│   ├── chat_interface.py
│   ├── sidebar.py
│   ├── chat_utils.py        # Thread/history management
│   └── styles.py            # Global CSS theme
└── assets/                  # Static images
```

##  Getting Started

### Prerequisites

*   **Docker** (Recommended) OR **Python 3.12**
*   **NVIDIA API Key**
*   **Pinecone API Key** & Index
*   **MongoDB Instance** (URI)

### Environment Setup

Create a `.env` file in the root directory:

```env
NVIDIA_API_KEY=your_nvidia_key
PINECONE_API_KEY=your_pinecone_key
mongodb_uri=your_mongodb_connection_string
database_name=your_database_name
```

### Installation & Run

#### Option A: Docker (Recommended)

1.  **Build and Start**:
    ```bash
    docker compose up --build
    ```
2.  **Access App**: Open [http://localhost:8501](http://localhost:8501) in your browser.

#### Option B: Local Python

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run Application**:
    ```bash
    streamlit run app.py
    ```

##  Usage Examples

DineLytics handles a wide range of business queries. Try asking:

*   **Sales Performance**: *"What were the total sales for Pizza last month?"*
*   **Trends**: *"Show me the daily revenue trend for November 2025."*
*   **Top Performers**: *"What are the top 5 best-selling products across all stores?"*
*   **Operational**: *"Which stores had the highest delivery fees last week?"*

##  Configuration

*   **Schemas**: Manage collection mappings in `schemas/schema.yaml`.
*   **Query Pipeline**: Tune the direct query pipeline in `query_pipeline.py`.

---
