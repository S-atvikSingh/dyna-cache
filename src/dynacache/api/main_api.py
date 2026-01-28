from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated
from src.dynacache.main import DynaCache

app = FastAPI(title="Dyna-Cache Semantic Interceptor")

# 1. Create a Singleton-like instance provider
_cache_instance = None

def get_cache_service():
    global _cache_instance
    if _cache_instance is None:
        # This only runs the first time the API is called
        _cache_instance = DynaCache()
    return _cache_instance

# 2. Schema Definitions
class QueryRequest(BaseModel):
    prompt: str

class QueryResponse(BaseModel):
    response: str
    status: str
    distance: str = "N/A"
    latency_ms: str

# 3. Routes using Dependency Injection
@app.post("/v1/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest, 
    # This 'Depends' tells FastAPI to fetch the cache instance for us
    cache: Annotated[DynaCache, Depends(get_cache_service)]
):
    try:
        result = cache.query(request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Middleware Error: {str(e)}")

@app.get("/health")
async def health(cache: Annotated[DynaCache, Depends(get_cache_service)]):
    return {
        "status": "healthy",
        "cache_size": len(cache.store.metadata),
        "model": "all-MiniLM-L6-v2"
    }

@app.get("/v1/stats")
async def get_stats(cache: Annotated[DynaCache, Depends(get_cache_service)]):
    # Fetch stats from Redis
    hits = int(cache.store.redis_client.get("stats:total_hits") or 0)
    misses = int(cache.store.redis_client.get("stats:total_misses") or 0)
    ms_saved = float(cache.store.redis_client.get("stats:ms_saved") or 0.0)
    
    total_requests = hits + misses
    hit_rate = (hits / total_requests * 100) if total_requests > 0 else 0
    
    return {
        "total_requests": total_requests,
        "hit_rate": f"{hit_rate:.2f}%",
        "estimated_time_saved_sec": f"{ms_saved / 1000:.2f}s",
        "estimated_cost_saved_usd": f"${(hits * 0.02):.4f}" # Assuming $0.02 per LLM call
    }