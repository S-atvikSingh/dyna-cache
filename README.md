# Dyna-Cache
A High-Performance Semantic Cache Middleware for LLMs

## Overview
Dyna-Cache is a developer-centric middleware designed to reduce LLM latency and API costs. Unlike traditional key-value caches that rely on exact string matching, Dyna-Cache utilizes vector similarity search to identify and serve semantically equivalent queries.

## Core Features
- Semantic Interception: Uses local transformer models to convert natural language into high-dimensional vectors.
- Vector Similarity Search: Leverages Facebook AI Similarity Search (FAISS) for sub-millisecond nearest-neighbor lookups.
- Persistent Storage: Implements local state management for vector indices and metadata, ensuring cache resiliency across restarts.
- Performance Telemetry: Integrated latency tracking and similarity scoring for production observability.

## System Architecture
The system follows a modular provider-consumer pattern:
1. Input: User query is intercepted by the DynaCache controller.
2. Embedding: Query is vectorized using the all-MiniLM-L6-v2 model (384 dimensions).
3. Search: FAISS index performs an L2 distance search against stored vectors.
4. Decision: If distance < 0.35, a HIT is returned from local storage. If not, a MISS is triggered, and the result is cached for future use.



## Technical Stack
- Language: Python 3.x
- Embedding Engine: Sentence-Transformers (all-MiniLM-L6-v2)
- Vector Store: FAISS (Facebook AI Similarity Search)
- Data Analysis: Pandas
- Persistence: Pickle / FAISS Binary Index

## Performance Benchmarks
Benchmarked on local hardware using a test suite of semantic variations:

| Metric | Result |
|--------|--------|
| Average Cache MISS Latency | 16.87 ms |
| Average Cache HIT Latency | 13.99 ms |
| Local Speedup Factor | 1.21x |

*Note: In production environments interfacing with remote LLM APIs (avg. 1s-5s latency), the effective speedup factor typically exceeds 70x.*

## Installation and Usage

1. Clone the repository:
   git clone [https://github.com/S-atvikSingh/dyna-cache.git](https://github.com/S-atvikSingh/dyna-cache.git)

2. Install dependencies:
   pip install -r requirements.txt

3. Initialize the package:
   pip install -e .

4. Run the benchmark:
   python -m tests.benchmark
