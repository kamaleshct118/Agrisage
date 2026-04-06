import os
from dotenv import load_dotenv
from crewai import Crew, Process
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import our custom tools (RAG & SQL)
from agent.tools import AgriculturalRAGTool, DatabaseSchemaTool, SQLExecutionTool

# Import our agents and routing logic
from agent.crew_agents import (
    create_intent_analyzer,
    create_rag_agent,
    create_sql_agent,
    create_response_agent
)
from agent.router import create_routing_tasks

def run_agriculture_agent(query: str):
    print(f"\n{'='*60}\n🚜 PROCESSING QUERY: '{query}'\n{'='*60}")
    
    # 1. Initialize Tools
    rag_tools = [AgriculturalRAGTool()]
    sql_tools = [DatabaseSchemaTool(), SQLExecutionTool()]
    
    # 2. Initialize Agents
    intent_agent = create_intent_analyzer()
    rag_agent = create_rag_agent(rag_tools)
    sql_agent = create_sql_agent(sql_tools)
    response_agent = create_response_agent()
    
    # 3. Initialize Tasks based on the Query
    tasks = create_routing_tasks(query, intent_agent, rag_agent, sql_agent, response_agent)
    
    # 4. Create the Crew
    agri_crew = Crew(
        agents=[intent_agent, rag_agent, sql_agent, response_agent],
        tasks=tasks,
        process=Process.sequential,
        verbose=True # Set to True so you can watch them "think" live!
    )
    
    # 5. Execute Pipeline!
    result = agri_crew.kickoff()
    
    print(f"\n{'='*60}\n🌟 FINAL ANSWER:\n{result}\n{'='*60}\n")
    return result

# ==========================================
# FastAPI Server Setup
# ==========================================
app = FastAPI(title="Agriculture AI Backend")

# Setup CORS so your React frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    route: str = "EXPLANATORY"
    sql: str = ""
    data: list = []
    
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    try:
        # 1. Initialize Tools
        rag_tools = [AgriculturalRAGTool()]
        sql_tools = [DatabaseSchemaTool(), SQLExecutionTool()]
        
        # 2. Initialize Agents (Must be instantiated ONCE)
        intent_agent = create_intent_analyzer()
        rag_agent = create_rag_agent(rag_tools)
        sql_agent = create_sql_agent(sql_tools)
        response_agent = create_response_agent()
        
        # 3. Create Crew with the exact same objects
        agri_crew = Crew(
            agents=[intent_agent, rag_agent, sql_agent, response_agent],
            tasks=create_routing_tasks(request.message, intent_agent, rag_agent, sql_agent, response_agent),
            process=Process.sequential,
            verbose=True
        )
        
        result = agri_crew.kickoff()
        
        # Pull details from the specific tasks for the frontend sidebar
        route = "EXPLANATORY"
        sql_query = ""
        
        for task_output in result.tasks_output:
            desc = task_output.description.lower()
            if "analyze the user query" in desc:
                raw_route = str(task_output.raw).upper().strip()
                # Check only the very last word generated to avoid catching the word 'analytical' in the paragraph
                last_word = raw_route.split()[-1] if raw_route.split() else ""
                
                if "HYBRID" in last_word:
                    route = "HYBRID"
                elif "ANALYTICAL" in last_word:
                    route = "ANALYTICAL"
                else:
                    route = "EXPLANATORY"
                    
            if "write and execute sql" in desc:
                # Basic check if it contains a SELECT
                raw_sql = str(task_output.raw)
                if "SELECT" in raw_sql.upper():
                    sql_query = raw_sql

        return ChatResponse(
            response=str(result.raw),
            route=route,
            sql=sql_query,
            data=[] # Can be expanded if we capture raw tool output
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Agriculture AI API is running!"}

if __name__ == "__main__":
    import uvicorn
    # Make sure we don't crash without the basic variable 
    load_dotenv()
    if not os.environ.get("GROQ_API_KEY"):
        print("CRITICAL ERROR: GROQ_API_KEY is missing from your .env file!")
        exit(1)
        
    print("🚀 Starting Agriculture API on http://localhost:8000 ...")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
