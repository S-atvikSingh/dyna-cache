from src.dynacache.core.embedder import EmbeddingEngine
from src.dynacache.core.vector_store import VectorStore

engine = EmbeddingEngine()
store = VectorStore()

# 1. Cache an answer
vec, _ = engine.encode("What is Python?")
store.add(vec, "Python is a high-level programming language.")

# 2. Query with a SIMILAR but DIFFERENT question
query_vec, _ = engine.encode("Tell me about the Python language")
match, dist = store.search(query_vec)

print(f"Match Found: {match}")
print(f"Distance Score: {dist:.4f}")