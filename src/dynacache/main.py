import time
from src.dynacache.core.embedder import EmbeddingEngine
from src.dynacache.core.vector_store import VectorStore

class DynaCache:
    def __init__(self, threshold=0.35):
        self.engine = EmbeddingEngine()
        self.store = VectorStore()
        # Attempt to load existing cache
        if self.store.load():
            print("Successfully restored cache from local storage.")
        else:
            print("No existing cache found. Starting fresh.")
        
        self.threshold = threshold

    def query(self, user_query: str):
        start_time = time.perf_counter()
        
        # 1. Generate embedding
        query_vec, _ = self.engine.encode(user_query)
        
        # 2. Check Cache
        match, distance = self.store.search(query_vec, threshold=self.threshold)
        
        if match:
            latency = time.perf_counter() - start_time
            return {
                "response": match,
                "status": "HIT",
                "distance": f"{distance:.4f}",
                "latency_ms": f"{latency * 1000:.2f}"
            }
        
        # 3. Simulate LLM Call (Cache Miss)
        llm_response = f"Generated Response for: {user_query}" 
        self.store.add(query_vec, llm_response)
        
        latency = time.perf_counter() - start_time
        return {
            "response": llm_response,
            "status": "MISS",
            "latency_ms": f"{latency * 1000:.2f}"
        }

if __name__ == "__main__":
    cache = DynaCache()
    # First query (MISS)
    print(cache.query("How do I learn Python?"))
    # Second similar query (HIT)
    print(cache.query("Best way to learn Python?"))