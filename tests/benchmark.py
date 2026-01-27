import time
import pandas as pd
from src.dynacache.main import DynaCache

def run_benchmark():
    cache = DynaCache(threshold=0.35)
    queries = [
        "What is the capital of France?",
        "Tell me the capital of France",  # Semantic Hit
        "How do I bake a cake?",
        "Recipe for a cake",              # Semantic Hit
        "What is 2+2?",
        "Result of 2 plus 2",             # Semantic Hit
        "Who wrote Romeo and Juliet?",
        "Author of Romeo and Juliet"      # Semantic Hit
    ]
    
    results = []

    print("\n--- Starting Benchmark ---")
    for q in queries:
        res = cache.query(q)
        results.append({
            "Query": q,
            "Status": res['status'],
            "Latency_ms": float(res['latency_ms'])
        })
    
    df = pd.DataFrame(results)
    
    # Calculate Stats
    avg_hit = df[df['status'] == 'HIT']['Latency_ms'].mean()
    avg_miss = df[df['status'] == 'MISS']['Latency_ms'].mean()
    
    print("\n--- Results Summary ---")
    print(df)
    print(f"\nAverage Cache MISS Latency: {avg_miss:.2f} ms")
    print(f"Average Cache HIT Latency: {avg_hit:.2f} ms")
    print(f"Speedup Factor: {avg_miss / avg_hit:.2f}x")

if __name__ == "__main__":
    run_benchmark()