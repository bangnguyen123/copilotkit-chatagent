from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from uuid import uuid4
import json
import chromadb

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
persistent_client = chromadb.PersistentClient()

# Delete and recreate the collection
persistent_client.delete_collection("employees")
collection = persistent_client.create_collection("employees")

# Now initialize Chroma AFTER the collection exists
vector_store_from_client = Chroma(
    client=persistent_client,
    collection_name="employees",
    embedding_function=embeddings,
)

# Load JSON file
with open("employees.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert entries to documents
documents = []
for item in data:
    content = (
        f"{item['name']} is a {item['level']} {item['role']} skilled in {item['skill']}. "
        f"They are {item['age']} years old, speak {item['foreign_language']}, "
        f"hold certification(s): {item['certs']}, and are based in {item['location']}."
    )
    documents.append(Document(page_content=content, metadata={"name": item["name"]}))

print(f"Loaded {len(documents)} structured documents.")

# Split content
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100,
    chunk_overlap=20
)
doc_splits = text_splitter.split_documents(documents)

print(f"Generated {len(doc_splits)} text chunks for embedding.")

# Embed and store
uuids = [str(uuid4()) for _ in range(len(doc_splits))]
vector_store_from_client.add_documents(documents=doc_splits, ids=uuids)
