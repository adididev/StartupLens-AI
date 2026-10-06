# MarketMind AI – Startup Intelligence Engine

An end-to-end AI system that uses Retrieval-Augmented Generation (RAG), web scraping, FAISS vector database, open-source embeddings, Groq-hosted LLM inference, and an intelligent scoring engine to analyze startup ideas.

## Features

- **Web Data Pipeline** – Scrapes DuckDuckGo and Wikipedia for real-time market context
- **RAG Engine** – FAISS vector search + sentence-transformers embeddings for semantic retrieval
- **Smart Scoring** – Min-max normalized metrics for demand, competition, growth, monetization & viability
- **LLM Analysis** – Groq-powered (LLaMA 3.3 70B) structured market insights
- **Beautiful UI** – Premium dark-themed Streamlit dashboard with animated metric cards

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector DB | FAISS |
| LLM | Groq API (LLaMA 3.3 70B) |
| Scraping | BeautifulSoup4 + Requests |
| ML Scoring | Custom heuristic engine |

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/marketmind-ai.git
   cd marketmind-ai
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your Groq API key
   ```

5. Run the app:
   ```bash
   streamlit run app.py
   ```

## Deploying to Streamlit Cloud

1. Push your code to GitHub (the `.gitignore` already excludes `.env` and secrets)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. In the app settings, go to **Secrets** and add:
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key"
   GROQ_MODEL = "llama-3.3-70b-versatile"
   GROQ_FALLBACK_MODEL = "llama-3.1-8b-instant"
   ```
5. Deploy!

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | ✅ Yes | — | Your Groq API key |
| `GROQ_MODEL` | No | `llama-3.3-70b-versatile` | Primary LLM model |
| `GROQ_FALLBACK_MODEL` | No | `llama-3.1-8b-instant` | Fallback if primary hits rate limits |

## Project Structure

```
marketmind/
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
