# AgriMind: CrewAI Architecture and System State Flow

This document details the exact class interfaces, abstract routing mechanisms, and multi-agent pipeline logic executing in the CrewAI ecosystem.

## 1. System Process Loop
The backend architecture implements `process=Process.sequential` inside the core `Crew` instance (`app.py`). Information is strictly passed linearly down the pipeline using bounded context arrays. There is no asynchronous tool concurrency; each agent blocks until completion before yielding thread control.

---

## 2. Agent Configurations & Memory Context

### Agent 1: `Agricultural Intent Analyst`
*   **Engine**: `groq/llama-3.1-8b-instant`
*   **Tool Access**: None
*   **System Prompt Boundary**: Constrained to NLP classification. 
*   **Action**: Evaluates user query string to detect deterministic data intent (numeric/statistical data) vs heuristic intent (methods, logic, reasons).
*   **Output State**: Hard-constrained to exactly one string: `EXPLANATORY`, `ANALYTICAL`, or `HYBRID`. This string is intercepted by the Fastapi JSON marshalling system strictly to handle Frontend conditional UI component mounting (Rendering Ragas Dials vs SQL codeblocks).

### Agent 2: `Agronomist Knowledge Expert`
*   **Engine**: `groq/llama-3.1-8b-instant`
*   **Tool Access**: `agricultural_knowledge_search`
*   **Operation Framework**: Executes a k-NN search against `faiss_index.bin` via `sentence-transformers/all-MiniLM-L6-v2`. Extracts top-K `k=3` relevant text chunks.
*   **Execution Strategy**: Always executes. If the semantic distance exceeds the local threshold (e.g. user asks a pure math question), it yields an empty state block.

### Agent 3: `Farming Data Scientist`
*   **Engine**: `groq/llama-3.1-8b-instant`
*   **Tool Access**: `Agriculture Database Schema Viewer`, `Agriculture SQL Execution Engine`
*   **Agent Logic**: 
    1. Triggers Tool 1 (`Schema Viewer`) to load DDL (Data Definition Language) definitions into the LLM context window. Prevents hallucinating column targets (`crop_production`, `npk_data`).
    2. Writes a valid `sqlite3` query mapping locally to `agri.db` using Tool 2 (`SQL Execution Engine`).
    3. Receives serialized JSON payload from the DB cursor execution.
*   **Conditional Soft-Skip Mechanism**: Due to standard `Process.sequential` limitations in CrewAI, bypassing this agent dynamically via standard Python arrays is impossible without dropping Hybrid support. Instead, a prompt heuristic ("Soft-Skip") dictates: "*If the query contains no data requirements, immediately output 'No data was needed.' without binding the sqlite logic.*". 

### Agent 4: `Agri-Tech Communicator` 
*   **Tool Access**: None
*   **Context Dependency**: Bounded context dynamically imports outputs (`context=[rag_task, sql_task]`). 
*   **Resolution Strategy**: Serves as the aggregation layer. Evaluates state objects from Agent 2 and Agent 3. Explicitly drops the `No data was needed` exception logic strings. Fuses both data outputs (raw statistics + FAISS chunks) into a comprehensive standard CommonMark syntax string representing the system's final HTTP response payload.

---

## 3. Abstract Tool Definitions (`tools.py`)

*   **`AgriDatabase.get_database_schema(self)`**: Acts as an inline Prompt-Injector. Returns explicit schema definitions map + hidden prompting constraints to direct specific Table utilization patterns (e.g., instructing the model to default queries evaluating yield patterns directly to `crop_production`).
*   **`AgriDatabase.execute_sql_query(self, query: str)`**: Direct native execution. Contains an exception loop mechanism—if SQL raises python syntax errors, it propagates the full Python Stack Trace as a standard string to the LLM agent, allowing standard `max_iter` loop-backs where the LLM automatically attempts to debug its own code within the framework iteration limit (default `max_iter=2`).
