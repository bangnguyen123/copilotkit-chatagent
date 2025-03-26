# test_retriever.py

from agent.retrieve_agent import get_or_create_retriever
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
persistent_client = chromadb.PersistentClient()
vector_store_from_client = Chroma(
    client=persistent_client,
    collection_name="employees",
    embedding_function=embeddings,
)
query = "How many senior dev"
retriever = vector_store_from_client.as_retriever()
results = retriever.invoke(query)

print(f"\nTop results for: {query}\n")
for i, doc in enumerate(results):
    print(f"[{i+1}] {doc.page_content[:300]}...\n")
