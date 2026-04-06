import argparse
import sys
import os

# Add the parent directory to sys.path so we can import rag module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.vector_store import AgriculturalVectorStore

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build or test the Agricultural RAG Vector Store")
    parser.add_argument("--build", action="store_true", help="Build the FAISS index from the dataset")
    parser.add_argument("--query", type=str, help="Search query to test the index")
    
    args = parser.parse_args()
    
    DATA_JSON = "data/raw/agriculture_data_Rag.json"
    INDEX_PATH = "data/processed/faiss_index.bin"
    META_PATH = "data/processed/metadata.json"
    
    store = AgriculturalVectorStore(index_path=INDEX_PATH, metadata_path=META_PATH)
    
    if args.build:
        store.build_index(DATA_JSON)
    elif args.query:
        print(f"\nSearching for: '{args.query}'\n")
        results = store.search(args.query, top_k=3)
        for i, res in enumerate(results):
            print(f"--- Result {i+1} (Distance Score: {res['score']:.4f}) ---")
            print(res['document']['chunk'])
            print()
    else:
        print("Please specify --build to create the index, or --query 'your question' to search.")
