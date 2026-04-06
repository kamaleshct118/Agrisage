import os
from crewai import Agent, LLM
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq LLM natively in CrewAI
default_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    temperature=0.3,
    api_key=os.environ.get("GROQ_API_KEY")
)

def create_intent_analyzer(llm=default_llm):
    return Agent(
        role="Agricultural Intent Analyst",
        goal="Determine whether a user's question requires explanatory knowledge, statistical SQL data, or both.",
        backstory=(
            "An expert linguist who parses questions from farmers. You know that queries like "
            "'how to improve yield' need the RAG Knowledge Base, while queries like 'production in Assam' "
            "need the SQL Database."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=2,
        llm=llm
    )

def create_rag_agent(tools, llm=default_llm):
    return Agent(
        role="Agronomist Knowledge Expert",
        goal="Provide factual, best-practice farming advice using specialized agricultural context.",
        backstory=(
            "An experienced agronomist. When asked a question, you ALWAYS use the 'Agricultural Knowledge Search' tool "
            "to find the 3 best answers, then you summarize them clearly for the farmer."
        ),
        tools=tools,
        verbose=True,
        allow_delegation=False,
        max_iter=2,
        llm=llm
    )

def create_sql_agent(tools, llm=default_llm):
    return Agent(
        role="Farming Data Scientist",
        goal="Write perfect SQL queries to extract exact crop production numbers or soil NPK requirements.",
        backstory=(
            "Meticulous data analyst. You ALWAYS start by using the 'Agriculture Database Schema Viewer' tool. "
            "IMPORTANT: Once you know the columns, use the 'Agriculture SQL Execution Engine' to get the exact data needed. "
            "NEVER SELECT giant lists of data. ALWAYS use SUM(), AVG(), or `LIMIT 10` so you don't run out of token space."
        ),
        tools=tools,
        verbose=True,
        allow_delegation=False,
        max_iter=2,
        llm=llm
    )

def create_response_agent(llm=default_llm):
    return Agent(
        role="Agri-Tech Communicator",
        goal="Combine the raw database numbers and farming advice into one beautiful, easy-to-read final answer.",
        backstory=(
            "A friendly local extension officer. You take the dry statistics from the Data Scientist "
            "and the complex advice from the Agronomist and turn it into a single, perfect response."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=2,
        llm=llm
    )
