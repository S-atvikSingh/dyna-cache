# Dyna-Cache
A High-Performance Semantic Cache Middleware for LLMs

## Overview
Dyna-Cache is a high-performance semantic cache designed to reduce LLM latency and API costs. Unlike traditional caches that require exact string matches, Dyna-Cache uses vector similarity search to identify and serve responses for semantically equivalent queries. By intercepting requests and serving them from a distributed Redis-backed cache, it eliminates redundant calls to expensive model providers.

## Core Features
- Semantic Interception: Uses local transformer models to convert natural language into high-dimensional vectors.
- Vector Similarity Search: Leverages Facebook AI Similarity Search (FAISS) for sub-millisecond nearest-neighbor lookups.
- Distributed Architecture: Implements Redis for metadata persistence and hit/miss telemetry, allowing the cache to scale horizontally.
- Production Observability: Integrated tracking for hit rates, total latency saved, and estimated cost reduction.
- Containerized Deployment: Fully orchestrated with Docker and Docker Compose for environment parity.

## System Architecture
The system operates as an API-driven middleware:
1. Input: User query is received via the FastAPI /v1/query endpoint.
2. Embedding: The query is vectorized using the all-MiniLM-L6-v2 model.
3. Search: The FAISS index performs an L2 distance search.
4. Decision: If the distance is below the 0.35 threshold, a HIT is served from Redis.
5. MISS Logic: On a cache miss, the system simulates/calls the LLM, returns the result, and stores the new vector-response pair.



## Technical Stack
- Language: Python 3.12
- API Framework: FastAPI
- Embedding Engine: Sentence-Transformers (all-MiniLM-L6-v2)
- Vector Store: FAISS (Facebook AI Similarity Search)
- Metadata Store: Redis
- Infrastructure: Docker, Docker Compose

## Performance Benchmarks
Benchmarked on local hardware using a test suite of semantic variations:

| Metric | Result |
|--------|--------|
| Average Cache MISS Latency | 16.87 ms |
| Average Cache HIT Latency | 13.99 ms |
| Local Speedup Factor | 1.21x |

*Note: In production environments interfacing with remote LLM APIs (avg. 1s-5s latency), the effective speedup factor typically exceeds 70x.*

While local hit latency is measured in milliseconds, the true business value lies in the reduction of remote LLM overhead.

| Metric | Result |
|--------|--------|
| Average Remote LLM Latency | 1000ms - 5000ms |
| Average Cache HIT Latency | ~14 ms |
| Estimated Time Saved per HIT | > 98% |
| Cost Efficiency | $0.002 saved per cached request (estimated) |


## Installation and Usage

1. Clone the repository:
   git clone [https://github.com/S-atvikSingh/dyna-cache.git](https://github.com/S-atvikSingh/dyna-cache.git)

2. Launch via Docker (Recommended): docker-compose up --build

3. Access Documentation: Navigate to http://localhost:8000/docs to interact with the API via Swagger UI.

4. Check Telemetry: Access http://localhost:8000/v1/stats to view real-time cache performance and cost savings.

## Future Roadmap
- RAG Context Normalization: Implement logic to separate the "User Query" from "Context Blocks" in prompts to improve hit rates for Retrieval-Augmented Generation workflows.
- Model Quantization: Optimize the embedding model using ONNX or TensorRT to further reduce CPU and memory footprints in containerized environments.
- Dynamic TTL (Time-To-Live): Integrate Redis expiration policies based on the "freshness" of the data or the frequency of cache hits.
- Multi-Tenant Support: Add API key authentication and namespace isolation for Redis keys to support multiple client applications.