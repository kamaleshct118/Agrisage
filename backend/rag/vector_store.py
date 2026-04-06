import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class AgriculturalVectorStore:
    def __init__(self, model_name='all-MiniLM-L6-v2', index_path='data/faiss_index.bin', metadata_path='data/metadata.json'):
        self.model = SentenceTransformer(model_name)
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.index = None
        self.metadata = []

    def load_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            print(f"Loaded existing index with {self.index.ntotal} vectors.")
            return True
        return False

    def build_index(self, json_file_path):
        print(f"Loading data from {json_file_path}...")
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"Processing {len(data)} records...")
        texts = []
        self.metadata = []
        
        # Better chunking: combining question and answer for complete cohesive context
        for item in data:
            question = item.get('input', '').strip()
            answer = item.get('response', '').strip()
            if question and answer:
                text_chunk = f"Question: {question}\nAnswer: {answer}"
                texts.append(text_chunk)
                self.metadata.append({"question": question, "answer": answer, "chunk": text_chunk})

        print("Generating embeddings (this may take a few minutes)...")
        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        
        dimension = embeddings.shape[1]
        print(f"Initializing FAISS index with dimension {dimension}...")
        self.index = faiss.IndexFlatL2(dimension)
        
        # Add embeddings to the index
        self.index.add(embeddings)
        print(f"Successfully added {self.index.ntotal} vectors to FAISS index.")

        # Save the index and metadata
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=4)
        print(f"Saved FAISS index to {self.index_path} and metadata to {self.metadata_path}.")

    def search(self, query, top_k=3):
        if self.index is None:
            if not self.load_index():
                raise ValueError("Index is not built or loaded yet.")
        
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                results.append({
                    "score": float(distances[0][i]),
                    "document": self.metadata[idx]
                })
        return results

