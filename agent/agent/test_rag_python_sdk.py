from ragflow_sdk import RAGFlow
import openai
import os
from dotenv import load_dotenv
import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
import os
import json
import chromadb
load_dotenv() # pylint: disable=wrong-import-position

# Your OpenAI API key (replace with your actual key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
persistent_client = chromadb.PersistentClient()
vector_store_from_client = Chroma(
    client=persistent_client,
    collection_name="employees",
    embedding_function=embeddings,
)
def get_openai_response(user_input):
    try:
        # Step 1: Search in Chroma
        relevant_docs = vector_store_from_client.similarity_search(
            query=user_input,
            k=5  # adjust as needed
        )
        print(relevant_docs)
        # Step 2: Build context from retrieved documents
        context = "\n---\n".join(doc.page_content for doc in relevant_docs)

        # Step 3: Construct system prompt
        system_prompt = f"""
        You are a helpful assistant with access to a dataset of employees. Use the following data to answer questions accurately:

        {context}

        Answer questions based solely on this data unless instructed otherwise. Provide clear and concise responses.
        """

        # Step 4: Send to OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    user_input = "I need employee who has Python skill"
    response = get_openai_response(user_input)
    print(f"Assistant: {response}")

main()