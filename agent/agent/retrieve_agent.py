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
import os

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
import chromadb

from dotenv import load_dotenv
load_dotenv() # pylint: disable=wrong-import-position


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)
persistent_client = chromadb.PersistentClient()
vector_store_from_client = Chroma(
    client=persistent_client,
    collection_name="employees",
    embedding_function=embeddings,
)
relevant_docs = vector_store_from_client.similarity_search(
    query="How many senior devs?",
    k=5  # adjust as needed
)

class AgentState(CopilotKitState):
    """
    Here we define the state of the agent

    In this instance, we're inheriting from CopilotKitState, which will bring in
    the CopilotKitState fields.
    """
    language: Literal["english", "spanish"] = "english"


@tool
def retrieve_employee(question: str):
    """Retrieve imployee with skill and their from chroma

    Args:
        question: user question
    """
    try:
        relevant_docs = vector_store_from_client.similarity_search(query=question, k=5)
        context = "\n---\n".join(doc.page_content for doc in relevant_docs)
        return context

    except Exception as e:
        print(f"Error occurred while retrieving chunks: {str(e)}")
        return None

tools = [retrieve_employee]

async def chat_node(state: AgentState, config: RunnableConfig) -> Command[Literal["tool_node", "__end__"]]:
    model = ChatOpenAI(
            model="openai/gpt-4",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),  # Your OpenRouter API key
            openai_api_base="https://openrouter.ai/api/v1"  # OpenRouter API endpoint
        )

    model_with_tools = model.bind_tools(
        [
            *state["copilotkit"]["actions"],
            retrieve_employee
        ],
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
