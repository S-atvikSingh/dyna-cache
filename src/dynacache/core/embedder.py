from sentence_transformers import SentenceTransformer
import time

class EmbeddingEngine:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the local transformer model.
        """
        print(f"Loading model: {model_name}...")
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str):
        """
        Converts input text into a numerical vector (embedding).
        """
        start_time = time.perf_counter()
        vector = self.model.encode(text)
        duration = time.perf_counter() - start_time
        
        return vector, duration

if __name__ == "__main__":
    # Quick smoke test
    engine = EmbeddingEngine()
    vec, latency = engine.encode("How is the weather?")
    print(f"Vector Dimensions: {vec.shape}")
    print(f"Encoding Latency: {latency:.4f} seconds")