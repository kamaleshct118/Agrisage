from crewai import Task

def create_routing_tasks(user_query, intent_agent, rag_agent, sql_agent, response_agent):
    """
    Defines the CrewAI tasks given a specific user query.
    """
    
    # Task 1: Analyze the Intent
    analyze_task = Task(
        description=(
            f"Analyze the user query: '{user_query}'. "
            "If it asks for exact numbers, averages, states, or crop requirements, say 'ANALYTICAL'. "
            "If it asks how to do something, best practices, or 'why', say 'EXPLANATORY'. "
            "If it asks for both data and advice, say 'HYBRID'."
        ),
        expected_output="A single word: EXPLANATORY, ANALYTICAL, or HYBRID.",
        agent=intent_agent
    )
    
    # Task 2: Gather RAG context (Advice)
    rag_task = Task(
        description=f"Using your search tools, find the best farming methods or explanatory advice regarding: '{user_query}'.",
        expected_output="A robust paragraph summarizing the farming advice from the knowledge base.",
        agent=rag_agent,
    )
    
    # Task 3: Gather SQL context (Data)
    sql_task = Task(
        description=f"Write and execute SQL to pull any exact statistical data or precise NPK numbers requested in: '{user_query}'.",
        expected_output="The raw data numbers and statistics pulled from the SQL database. State if no data was needed.",
        agent=sql_agent
    )
    
    # Task 4: Final Synthesis
    synthesize_task = Task(
        description=(
            f"Review the original query: '{user_query}'.\n"
            f"Using the context from the Agronomist and the Data Scientist, write the final perfect response. "
            f"Ignore any 'No data needed' messages from the data scientist if they didn't pull SQL data, just focus on the useful information."
        ),
        expected_output="A highly readable, comprehensive final answer formatted cleanly for the user.",
        agent=response_agent,
        context=[rag_task, sql_task] 
    )
    
    return [analyze_task, rag_task, sql_task, synthesize_task]
