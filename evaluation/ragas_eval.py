import os
import sys
import json
import random
import pandas as pd
from dotenv import load_dotenv

# Path setup to import backend modules
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(base_dir, "backend")
sys.path.append(backend_dir)

# Automatically switch working directory so simple 'data/...' paths resolve flawlessly
os.chdir(backend_dir)

# Load environment variables FIRST so CrewAI and tools can initialize
load_dotenv(os.path.join(backend_dir, ".env"))

# FIX: Remove API_BASE from env to prevent Ragas/ChatGroq from doubling the /openai/v1 path 
if "GROQ_API_BASE" in os.environ:
    del os.environ["GROQ_API_BASE"]
if "OPENAI_API_BASE" in os.environ:
    del os.environ["OPENAI_API_BASE"]

if not os.environ.get("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY missing from .env")

# Now import the necessary backend components safe from ModuleNotFound errors
from app import run_agriculture_agent
from agent.tools import rag_store

# Ragas & Langchain
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

def run_evaluation():
    print("="*60)
    print("🚀 INITIALIZING RAGAS EVALUATION PIPELINE")
    print("="*60)
    
    # 1. Setup Ragas LLM and Embeddings wrappers
    # We use Groq to mathematically grade the results, and the local HuggingFace model for distance scoring
    print("[1] Configuring RAGAS with Groq LLM and local HuggingFace Embeddings...")
    groq_llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0) 
    hf_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 2. Extract Test Data
    print("[2] Loading Test Dataset from JSON...")
    data_path = os.path.join(backend_dir, "data", "raw", "agriculture_data_Rag.json")
    with open(data_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        
    # We pick 2 random samples for a quick evaluation test so it doesn't run for hours
    sample_data = random.sample(raw_data, min(2, len(raw_data)))
    
    questions = []
    answers = []
    contexts = []
    ground_truths = []
    
    print(f"\n[3] Running CrewAI Agents on {len(sample_data)} Questions...")
    for idx, item in enumerate(sample_data):
        question = item.get('input', '').strip()
        ground_truth = item.get('response', '').strip()
        
        if not question or not ground_truth:
            continue
            
        print(f"\n--- Evaluating Q{idx+1}: {question[:50]}... ---")
        
        # A. Grab Contexts directly from our Engine (simulate exactly what FAISS retrieves)
        search_results = rag_store.search(question, top_k=3)
        retrieved_contexts = [res['document']['answer'] for res in search_results]
        
        # B. Grab the AI's final answer using standard CrewAI trigger
        final_answer = run_agriculture_agent(question)
        
        # C. Save variables to the lists
        questions.append(question)
        contexts.append(retrieved_contexts)
        answers.append(str(final_answer))
        ground_truths.append(ground_truth) # Use string for newer Ragas versions reference
        
    # 3. Build HuggingFace Dataset
    print("\n[4] Constructing RAGAS HF Evaluation Dataset...")
    data_dict = {
        "user_input": questions,
        "response": answers,
        "retrieved_contexts": contexts,
        "reference": ground_truths
    }
    dataset = Dataset.from_dict(data_dict)
    
    # 4. Evaluate using RAGAS
    print("[5] Running RAGAS Evaluation... (This may take a minute ⏳)")
    result = evaluate(
        dataset=dataset,
        metrics=[Faithfulness(), AnswerRelevancy(), ContextPrecision(), ContextRecall()],
        llm=groq_llm,
        embeddings=hf_embeddings
    )
    
    # 5. Output Results
    print("\n" + "="*60)
    print("📊 FINAL RAGAS EVALUATION SCORES")
    print("="*60)
    df = result.to_pandas()
    
    # Format and print the clean DataFrame table
    print(df[['user_input', 'faithfulness', 'answer_relevancy', 'context_precision', 'context_recall']].to_string())
    
    # Save the dataframe for later visualization
    os.makedirs(os.path.join(base_dir, "evaluation"), exist_ok=True)
    output_path = os.path.join(base_dir, "evaluation", "evaluation_results.csv")
    df.to_csv(output_path, index=False)
    print(f"\n✅ Full results safely exported to: {output_path}")

if __name__ == "__main__":
    run_evaluation()
