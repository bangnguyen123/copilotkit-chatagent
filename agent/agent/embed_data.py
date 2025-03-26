from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from uuid import uuid4
import json
import chromadb

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
persistent_client = chromadb.PersistentClient()
vector_store_from_client = Chroma(
    client=persistent_client,
    collection_name="employees",
    embedding_function=embeddings,
)
collection = persistent_client.get_or_create_collection("employees")
# Load JSON file
with open("employees.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Turn each structured entry into a full sentence (or paragraph)
documents = []
for item in data:
    content = (
        f"{item['name']} is a {item['level']} {item['role']} skilled in {item['skill']}. "
        f"They are {item['age']} years old, speak {item['foreign_language']}, "
        f"hold certification(s): {item['certs']}, and are based in {item['location']}."
    )
    documents.append(Document(page_content=content, metadata={"name": item["name"]}))

print(f"Loaded {len(documents)} structured documents.")

# Split the content into chunks (can be skipped if each entry is short)
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100,
    chunk_overlap=20
)
doc_splits = text_splitter.split_documents(documents)

print(f"Generated {len(doc_splits)} text chunks for embedding.")

# Embed and store (assuming you’ve set up your vector store with an embedding function)
uuids = [str(uuid4()) for _ in range(len(doc_splits))]
vector_store_from_client.add_documents(documents=doc_splits, ids=uuids)
