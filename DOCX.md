# Requirement
- Build a simple chatbot that can retrieve employee information
- Tool: CopilotKit, Langgraph, OpenRouter, RagFlow

# Architecture
```mermaid
graph LR;
    
    subgraph Client["Client Interaction"]
        A["Client (Web App / Chatbot)"]
    end
    
    subgraph Backend["Backend Server"]
        B["FastAPI Server"]
    end
    
    subgraph LangGraph["LangGraph Agent"]
        C["Chat Node (LLM Processing)"]
        D["Tool Node (Execute Tools)"]
    end
    
    subgraph ExternalServices["External Services"]
        E["OpenRouter (LLM API)"]
        F["RAGFlow (Document Retrieval)"]
    end

    A -->|Sends Request| B -->|Processes Request| C;
    C -->|Calls LLM| E;
    C -- Needs External Data? --> D;
    D -->|Fetches Data| F;
    D -->|Returns Data| C;
    C -->|Final Response Sent| A;
```
# Tools:
1. Copilotkit
2. FastAPI
3. RAGFlow
4. OpenRouter
# Set-up
1. Get an example of CopilotKit
2. Set up local for Copilot Provider
3. Router 

