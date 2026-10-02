"""
L7 — Personal Knowledge Base  (STARTER)
========================================
Run with:
    python starter.py

Your goal: build a persistent ChromaDB knowledge base from course content and
demonstrate metadata-filtered semantic search.

Required features:
    1. A persistent ChromaDB client (data survives restarts)
    2. A collection called "my_knowledge" created with get_or_create_collection
    3. At least 15 documents from at least 3 different modules, each with:
       - A unique ID (e.g. "doc_01")
       - Text content (a sentence or short paragraph)
       - Metadata with at least `module` (e.g. "5") and `topic`
         (e.g. "api", "database", "frontend", "ai")
    4. A search() function that accepts a query and optional module filter
       and returns the top 5 results with distances and metadata
    5. At least 3 test queries:
       - One broad (no filter)
       - One filtered to a specific module
       - One where the query words differ from the stored documents

Key concepts:
    Persistent client:
        client = chromadb.PersistentClient(path="./chroma_db")

    Upsert avoids errors on re-runs:
        collection.upsert(ids=[...], documents=[...], metadatas=[...])

    Metadata filtering:
        collection.query(
            query_texts=["your query"],
            n_results=5,
            where={"module": "5"}   # only return docs from module 5
        )

    Result structure:
        results["ids"][0]        # list of IDs
        results["documents"][0]  # list of document strings
        results["metadatas"][0]  # list of metadata dicts
        results["distances"][0]  # list of distances (lower = more similar)
"""

import chromadb

# ── Client & collection ──────────────────────────────────────────────────────
# TODO: Create a PersistentClient with path="./chroma_db"
client = chromadb.PersistentClient(path="./chroma_db")

# TODO: Get or create a collection called "my_knowledge"
collection = client.get_or_create_collection(
    name="my_knowledge",
    metadata={"description": "AI Engineering Foundations course content"}
)

print(f"Collection '{collection.name}' ready.")
print(f"Current document count: {collection.count()}")
# ── Documents 
documents = [
    # Module 3 - Databases
    "SQLAlchemy is a Python library that allows applications to interact with databases using Python objects.",
    "A foreign key connects a record in one database table to a record in another table.",
    "SQL JOIN operations can combine related data from multiple database tables.",
    "The GROUP BY clause organizes rows with the same values so aggregate functions can be used.",
    "Parameterized queries help prevent SQL injection by keeping user input separate from SQL commands.",

    # Module 4 - APIs
    "A REST API allows applications to communicate with each other using HTTP requests and responses.",
    "The GET HTTP method is commonly used to retrieve information from an API.",
    "The POST HTTP method is commonly used to create new data through an API.",
    "A 404 HTTP status code indicates that the requested resource could not be found.",
    "JSON is a common data format used for sending information between a client and an API.",

    # Module 5 - FastAPI and Authentication
    "FastAPI is a Python framework used to build web APIs quickly.",
    "FastAPI can use Pydantic models to validate incoming request data.",
    "JWT tokens can be used to authenticate users when they access protected API endpoints.",
    "A protected FastAPI endpoint can use a dependency to identify the currently authenticated user.",
    "CORS allows a frontend application running on one origin to communicate with a backend running on another origin."
]



# ────────────────────────────────────────────────────────────────
# TODO: Define three lists that match in length:
#   ids       — unique strings like "doc_01", "doc_02", ...
#   documents — text summaries from at least 3 different modules
#   metadatas — dicts with at least {"module": "X", "topic": "Y"}
#
# Aim for at least 15 documents.

ids = [
    # TODO
    "doc_01",
    "doc_02",
    "doc_03",
    "doc_04",
    "doc_05",
    "doc_06",
    "doc_07",
    "doc_08",
    "doc_09",
    "doc_10",
    "doc_11",
    "doc_12",
    "doc_13",
    "doc_14",
    "doc_15"
]

documents = [
    # TODO — one sentence or short paragraph per document
    # Module 3 - Databases
    "SQLAlchemy is a Python library used to interact with databases.",
    "A foreign key connects a record in one database table to a record in another table.",
    "SQL JOIN operations combine related data from multiple database tables.",
    "The GROUP BY clause organizes rows with the same values for aggregate calculations.",
    "Parameterized queries help prevent SQL injection by separating user input from SQL commands.",

    # Module 4 - APIs
    "A REST API allows applications to communicate with each other using HTTP requests and responses.",
    "The GET method is commonly used to retrieve information from an API.",
    "The POST method is commonly used to create new information through an API.",
    "A 404 HTTP status code means that the requested resource could not be found.",
    "JSON is a common format used to send data between a client and an API.",

    # Module 5 - FastAPI
    "FastAPI is a Python framework used to build web APIs.",
    "Pydantic models can validate data received by a FastAPI application.",
    "JWT tokens can be used to authenticate users when accessing protected API endpoints.",
    "FastAPI dependencies can be used to identify the currently authenticated user.",
    "CORS allows a frontend application to communicate with a backend on another origin."
]

metadatas = [
    # TODO — {"module": "1", "topic": "ai"}, {"module": "5", "topic": "api"}, ...
    {"module": "3", "topic": "database"},
    {"module": "3", "topic": "database"},
    {"module": "3", "topic": "database"},
    {"module": "3", "topic": "database"},
    {"module": "3", "topic": "security"},

    # Module 4
    {"module": "4", "topic": "api"},
    {"module": "4", "topic": "api"},
    {"module": "4", "topic": "api"},
    {"module": "4", "topic": "api"},
    {"module": "4", "topic": "api"},

    # Module 5
    {"module": "5", "topic": "fastapi"},
    {"module": "5", "topic": "validation"},
    {"module": "5", "topic": "authentication"},
    {"module": "5", "topic": "authentication"},
    {"module": "5", "topic": "frontend"}
]

# TODO: Upsert all documents into the collection
# Upsert all documents into the collection
collection.upsert(
    ids=ids,
    documents=documents,
    metadatas=metadatas
)
print(f"Stored {collection.count()} documents.")
# ── Search function ──────────────────────────────────────────────────────────
def search(query: str, module_filter: str = None, n_results: int = 5):
    """Return top results for query, optionally filtered to a specific module."""
    # TODO: Build the where dict only when module_filter is provided
    where = {"module": module_filter} if module_filter else None


    # TODO: Call collection.query() with query_texts, n_results, and where
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where
    )
    # TODO: Print each result's rank, distance, metadata, and document text
    for i in range(len(results["ids"][0])):
        print(f"\n{i + 1}. [distance: {results['distances'][0][i]:.4f}]")
        print(f"   ID: {results['ids'][0][i]}")
        print(f"   Metadata: {results['metadatas'][0][i]}")
        print(f"   Document: {results['documents'][0][i]}")

    return results


# ── Test queries ─────────────────────────────────────────────────────────────
print("=== Broad search (no filter) ===")
# TODO: Call search() with a broad query
search("How do applications communicate with each other?")
print("\n=== Filtered to a specific module ===")
# TODO: Call search() with a query and a module_filter
search("user authentication", module_filter="5")

print("\n=== Different words than stored documents ===")
# TODO: Call search() with a query that paraphrases rather than copies
#       the stored text — e.g. "how to handle bad user input" instead of
#       "Pydantic validates request data"
search("how to handle bad user input")