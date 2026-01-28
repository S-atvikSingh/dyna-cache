import time
from src.dynacache.core.embedder import EmbeddingEngine
from src.dynacache.core.vector_store import VectorStore

class DynaCache:
    def __init__(self, threshold=0.35):
        self.engine = EmbeddingEngine()
        # VectorStore now automatically loads the FAISS index and connects to Redis
        self.store = VectorStore()
        self.threshold = threshold

    def query(self, user_query: str):
        start_time = time.perf_counter()
        
        # 1. Generate embedding
        query_vec, _ = self.engine.encode(user_query)
        
        # 2. Check Cache
        match, distance = self.store.search(query_vec, threshold=self.threshold)
        
        # Telemetry tracking in Redis
        if match:
            latency = time.perf_counter() - start_time
            # Increment a global "HIT" counter in Redis
            self.store.redis_client.incr("stats:total_hits")
            # Log time saved (Assume LLM takes 1000ms)
            time_saved = 1000 - (latency * 1000)
            self.store.redis_client.incrbyfloat("stats:ms_saved", time_saved)
            
            return {
                "response": match,
                "status": "HIT",
                "distance": f"{distance:.4f}",
                "latency_ms": f"{latency * 1000:.2f}"
            }
        
        # 3. Cache Miss
        self.store.redis_client.incr("stats:total_misses")
        llm_response = f"Generated Response for: {user_query}" 
        self.store.add(query_vec, llm_response)
        
        latency = time.perf_counter() - start_time
        return {
            "response": llm_response,
            "status": "MISS",
            "latency_ms": f"{latency * 1000:.2f}"
        }