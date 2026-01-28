import faiss
import numpy as np
import redis
import json
import os

class VectorStore:
    def __init__(self, dimension: int = 384):
        # 1. Initialize FAISS for vector math
        self.index = faiss.IndexFlatL2(dimension)
        self.index_path = "config/faiss_store.index"
        
        # 2. Connect to Redis for metadata
        # decode_responses=True automatically converts bytes to strings
        redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_client = redis.Redis(
            host=redis_host, 
            port=6379, 
            db=0, 
            decode_responses=True
        )
        
        # Ensure config directory exists for the FAISS index
        os.makedirs("config", exist_ok=True)
        self.load_index()

    def add(self, vector, text_content):
        # Add to FAISS index
        vector = np.array([vector]).astype('float32')
        self.index.add(vector)
        
        # The 'ID' in FAISS is the current total minus 1
        new_id = self.index.ntotal - 1
        
        # Store metadata in Redis linked to that ID
        self.redis_client.set(f"cache_meta:{new_id}", text_content)
        
        # Save the FAISS index to disk (Redis handles its own persistence)
        faiss.write_index(self.index, self.index_path)

    def search(self, query_vector, threshold=0.35):
        query_vector = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query_vector, k=1)
        
        if indices[0][0] != -1:
            idx = indices[0][0]
            distance = distances[0][0]
            if distance < threshold:
                # Fetch only the specific piece of data we need from Redis
                match = self.redis_client.get(f"cache_meta:{idx}")
                return match, distance
        
        return None, None

    def load_index(self):
        """Loads the FAISS index from disk if it exists."""
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            print(f"Loaded FAISS index with {self.index.ntotal} vectors.")