# StartupLens AI – Startup Intelligence Engine

An end-to-end AI system that uses Retrieval-Augmented Generation (RAG), web scraping, FAISS vector database, open-source embeddings, Groq-hosted LLM inference, and an intelligent scoring engine to analyze startup ideas.

## Features

- **Web Data Pipeline** – Scrapes DuckDuckGo and Wikipedia for real-time market context
- **RAG Engine** – FAISS vector search + sentence-transformers embeddings for semantic retrieval
- **Smart Scoring** – Min-max normalized metrics for demand, competition, growth, monetization & viability
- **LLM Analysis** – Groq-powered (GPT-OSS 120B) structured market insights
- **Beautiful UI** – Premium dark-themed Streamlit dashboard with animated metric cards

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector DB | FAISS |
| LLM | Groq API (GPT-OSS 120B) |
| Scraping | BeautifulSoup4 + Requests |
| ML Scoring | Custom heuristic engine |

## Project Structure

```
StartupLens-AI/
├── app.py                  # Streamlit UI & orchestration
├── ml/
│   └── model.py            # Scoring engine (normalize, monetization, viability)
├── rag/
│   ├── embeddings.py       # Sentence-transformer embedding generation
│   ├── vector_store.py     # FAISS index creation & search
│   ├── retriever.py        # Semantic retrieval pipeline
│   └── generator.py        # Groq LLM API integration
├── scraping/
│   └── web_scraper.py      # DuckDuckGo + Wikipedia data fetching
├── utils/
│   ├── cleaning.py         # Text preprocessing
│   └── chunking.py         # Text chunking for embeddings
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```
