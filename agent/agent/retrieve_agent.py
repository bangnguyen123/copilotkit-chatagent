from typing_extensions import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from langgraph.prebuilt import ToolNode
from copilotkit import CopilotKitState
from ragflow_sdk import RAGFlow
import os
from dotenv import load_dotenv
load_dotenv() # pylint: disable=wrong-import-position


class AgentState(CopilotKitState):
    """
    Here we define the state of the agent

    In this instance, we're inheriting from CopilotKitState, which will bring in
    the CopilotKitState fields.
    """
    language: Literal["english", "spanish"] = "english"


@tool
def retrieve_chunks_from_ragflow(question: str):
    """Retrieve imployee from ragflow

    Args:
        question: user question
    """
    RAGFLOW_API_KEY = os.getenv("RAGFLOW_API_KEY")
    BASE_URL = os.getenv("BASE_URL")
    dataset_ids = ["1fa6807efdd811efb0fd0242c0a86b03"]  # Replace with your actual dataset ID
    document_ids = ["d8345272fe9311efb2910242c0a86b06"]  # Replace with your actual document ID
    rag_object = RAGFlow(api_key=RAGFLOW_API_KEY, base_url=BASE_URL)
    try:
        # Call the RAGFlow retrieve method
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

        # Return the list of chunks
        chunk_dicts = [
            {
                "content": chunk.content,  # Adjust based on actual attribute names
                "id": chunk.id,            # Include other relevant fields
            }
            for chunk in chunks
        ]
        return chunk_dicts

    except Exception as e:
        print(f"Error occurred while retrieving chunks: {str(e)}")
        return None


tools = [retrieve_chunks_from_ragflow]


async def chat_node(state: AgentState, config: RunnableConfig) -> Command[Literal["tool_node", "__end__"]]:
    # 1. Define the model
    model = ChatOpenAI(
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),  # Your OpenRouter API key
            openai_api_base="https://openrouter.ai/api/v1"  # OpenRouter API endpoint
        )

    model_with_tools = model.bind_tools(
        [
            *state["copilotkit"]["actions"],
            # get_weather,
            retrieve_chunks_from_ragflow
        ],

        # 2.1 Disable parallel tool calls to avoid race conditions,
        #     enable this for faster performance if you want to manage
        #     the complexity of running tool calls in parallel.
        parallel_tool_calls=False,
    )

    system_message = SystemMessage(
        content=f"You are a helpful assistant. Talk in {state.get('language', 'english')}."
    )

    response = await model_with_tools.ainvoke([
        system_message,
        *state["messages"],
    ], config)

    # Check for tool calls in the response and handle them. We ignore
    # CopilotKit actions, as they are handled by CopilotKit.
    if isinstance(response, AIMessage) and response.tool_calls:
        actions = state["copilotkit"]["actions"]

        # 5.1 Check for any non-copilotkit actions in the response and
        #     if there are none, go to the tool node.
        if not any(
            action.get("name") == response.tool_calls[0].get("name")
            for action in actions
        ):
            return Command(goto="tool_node", update={"messages": response})

    # 6. We've handled all tool calls, so we can end the graph.
    return Command(
        goto=END,
        update={
            "messages": response
        }
    )

workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)
workflow.add_node("tool_node", ToolNode(tools=tools))
workflow.add_edge("tool_node", "chat_node")
workflow.set_entry_point("chat_node")

graph = workflow.compile(MemorySaver())
