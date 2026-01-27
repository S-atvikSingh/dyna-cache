import faiss
import numpy as np

class VectorStore:
    def __init__(self, dimension: int = 384):
        """
        Initializes an IndexFlatL2 (Euclidean distance) index.
        Dimension 384 matches the all-MiniLM-L6-v2 model.
        """
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []  # Stores the actual text/answers linked to vectors

    def add(self, vector, text_content):
        # FAISS requires float32 and a specific shape (1, dimension)
        vector = np.array([vector]).astype('float32')
        self.index.add(vector)
        self.metadata.append(text_content)

    def search(self, query_vector, threshold=0.6):
        """
        Returns the closest match if it's within the similarity threshold.
        """
        query_vector = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query_vector, k=1)
        
        # indices[0][0] is -1 if no match found
        if indices[0][0] != -1:
            distance = distances[0][0]
            if distance < threshold:
                return self.metadata[indices[0][0]], distance
        
        return None, None