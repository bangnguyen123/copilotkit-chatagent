from ragflow_sdk import RAGFlow
import openai
import os
from dotenv import load_dotenv
import json
load_dotenv() # pylint: disable=wrong-import-position

# Your OpenAI API key (replace with your actual key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def retrieve_chunks_from_ragflow(question: str, dataset_ids: list, document_ids: list, api_key: str, base_url: str):
    rag_object = RAGFlow(api_key=api_key, base_url=base_url)

    try:
        chunks = rag_object.retrieve(
            question=question,
            dataset_ids=dataset_ids,
            document_ids=document_ids,
            page=1,  # You can change this if you want to paginate the results
            page_size=5,  # Set the number of chunks to retrieve (adjust as needed)
            similarity_threshold=0.2,  # Set the minimum similarity threshold
            vector_similarity_weight=0.3,  # Adjust vector similarity weight if needed
            top_k=1024,  # Set the number of chunks engaged in cosine similarity computation
            keyword=False,  # Disable keyword-based matching
        )

        chunk_dicts = [
            {
                "content": chunk.content,
                "id": chunk.id,
            }
            for chunk in chunks
        ]
        return chunk_dicts

    except Exception as e:
        print(f"Error occurred while retrieving chunks: {str(e)}")
        return None

# Function to get a response from OpenAI
def get_openai_response(user_input):
    RAGFLOW_API_KEY = os.getenv("RAGFLOW_API_KEY")
    BASE_URL = os.getenv("BASE_URL")
    dataset_ids = ["1fa6807efdd811efb0fd0242c0a86b03"]  # Replace with your actual dataset ID
    document_ids = ["d8345272fe9311efb2910242c0a86b06"]  # Replace with your actual document ID
    chunk_data = retrieve_chunks_from_ragflow(user_input, dataset_ids, document_ids, RAGFLOW_API_KEY, BASE_URL)

    context = json.dumps(chunk_data, indent=2)
    system_prompt = f"""
        You are a helpful assistant with access to a dataset of employees. Use the following data to answer questions accurately:

        {context}

        Answer questions based solely on this data unless instructed otherwise. Provide clear and concise responses.
    """
    try:
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
    user_input = "I need dev who has Python skill"
    response = get_openai_response(user_input)
    print(f"Assistant: {response}")
