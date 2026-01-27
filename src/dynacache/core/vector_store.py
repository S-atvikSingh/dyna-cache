import faiss
import numpy as np
import pickle
import os

class VectorStore:
    def __init__(self, dimension: int = 384):
        """
        Initializes FAISS index and sets up local storage paths.
        """
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []
        self.index_path = "config/faiss_store.index"
        self.meta_path = "config/metadata.pkl"
        
        os.makedirs("config", exist_ok=True)

    def add(self, vector, text_content):
        """Adds a vector to the index and persists to disk."""
        vector = np.array([vector]).astype('float32')
        self.index.add(vector)
        self.metadata.append(text_content)
        self.save()

    def search(self, query_vector, threshold=0.35):
        """
        Performs a K-Nearest Neighbor search.
        Returns the match if the distance is below the threshold.
        """
        query_vector = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query_vector, k=1)
        
        # Check if we have a valid index and if it's within our 'similarity' threshold
        if indices[0][0] != -1:
            distance = distances[0][0]
            if distance < threshold:
                return self.metadata[indices[0][0]], distance
        
        return None, None

    def save(self):
        """Persists FAISS index and metadata."""
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, 'wb') as f:
            pickle.dump(self.metadata, f)

    def load(self):
        """Loads index and metadata from disk."""
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, 'rb') as f:
                self.metadata = pickle.load(f)
            return True
        return False