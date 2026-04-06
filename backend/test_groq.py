import os
from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
load_dotenv()

# Pre-emptively disable telemetry so it doesn't crash on firewall blocks again!
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

print("Step 1: Initializing Groq LLM...")
# 1. Define the Groq LLM
groq_llm = LLM(
    model="llama-3.3-70b-versatile",
    
    # PUT YOUR *NEW* GROQ KEY HERE! (Do not paste it into the chat!)
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

print("Step 2: Defining the Test Agent...")
# 2. Assign the LLM to an agent
researcher = Agent(
    role='Researcher',
    goal='Discover insights about AI trends',
    backstory='An expert researcher with a focus on emerging technology.',
    llm=groq_llm,
    verbose=True
)

print("Step 3: Creating a simple test task...")
# 3. Create a quick, easy task to trigger the LLM
test_task = Task(
    description="Write exactly one short sentence explaining what a Large Language Model is.",
    expected_output="A single sentence about LLMs.",
    agent=researcher
)

# 4. Bind the agent to a crew safely
test_crew = Crew(
    agents=[researcher],
    tasks=[test_task],
    verbose=True
)

print("Step 4: Kicking off the CrewAI test! (Waiting for Groq response...)\n" + "-"*40)
try:
    result = test_crew.kickoff()
    print("\n" + "="*50)
    print("✅ SUCCESS! GROQ IS CONNECTED AND WORKING PERFECTLY!")
    print(f"Result:\n{result}")
    print("="*50)
except Exception as e:
    print("\n" + "❌"*25)
    print("API CALL FAILED! If it says 'invalid_api_key' below, Groq has revoked your key!")
    print(f"ERROR DETAILS:\n{e}")
    print("❌"*25)
