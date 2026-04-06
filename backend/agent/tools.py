from crewai.tools import BaseTool
import json
import os

# We will import our pre-built engines
from rag.vector_store import AgriculturalVectorStore
from sql.agri_db_tool import AgriDatabase

# Initialize our databases directly using the absolute paths we established
RAG_INDEX = 'data/processed/faiss_index.bin'
RAG_META = 'data/processed/metadata.json'
SQL_DB = 'data/processed/agri.db'

rag_store = AgriculturalVectorStore(index_path=RAG_INDEX, metadata_path=RAG_META)
sql_db = AgriDatabase(db_path=SQL_DB)


class AgriculturalRAGTool(BaseTool):
    name: str = "Agricultural Knowledge Search"
    description: str = (
        "Search the agricultural knowledge base for explanatory questions. "
        "Use this tool when answering 'How', 'Why', or general farming practice questions (e.g. soil health, best practices). "
        "The input should be the natural language question."
    )

    def _run(self, query: str) -> str:
        try:
            results = rag_store.search(query, top_k=3)
            # Combine the chunks into a readable string for the Agent
            formatted_results = "\n\n".join([f"[Source {i+1}]: {res['document']['answer']}" for i, res in enumerate(results)])
            return f"Found the following knowledge:\n{formatted_results}"
        except Exception as e:
            return f"Error retrieving information: {str(e)}"


class DatabaseSchemaTool(BaseTool):
    name: str = "Agriculture Database Schema Viewer"
    description: str = (
        "View the tables and columns available in the agriculture SQL Database. "
        "ALWAYS use this tool BEFORE trying to write a SQL query to verify column names. "
        "Pass an empty string as input."
    )

    def _run(self, dummy: str = "") -> str:
        return sql_db.get_database_schema()


class SQLExecutionTool(BaseTool):
    name: str = "Agriculture SQL Execution Engine"
    description: str = (
        "Execute raw SQL queries against the agriculture database to gather analytical data. "
        "Use this tool to find exact numbers, calculate averages, filter by crop or state, and perform JOINs. "
        "Input MUST be a pure, strictly valid SQL query string without formatting markdown."
    )

    def _run(self, query: str) -> str:
        # Strip any accidental ```sql markdown the LLM might have generated
        clean_query = query.replace("```sql", "").replace("```", "").strip()
        result = sql_db.execute_sql_query(clean_query)
        
        if isinstance(result, dict) and "sql_error" in result:
            return f"Query Failed with Error: {result['sql_error']}. Consider using the Schema Viewer tool to check your columns."
            
        return f"Query Succeeded! Results data:\n{json.dumps(result, indent=2)}"
