import streamlit as st
import time
from dotenv import load_dotenv

from scraping.web_scraper import fetch_web_data
from utils.cleaning import clean_text
from utils.chunking import chunk_text
from rag.embeddings import get_embeddings
from rag.vector_store import create_index, search
from rag.retriever import retrieve
from rag.generator import generate_response
from ml.model import compute_all_scores

# Load variables from a local .env file if present.
load_dotenv()


def get_label(score):
    if score > 70:
        return "🟢 High"
    elif score > 40:
        return "🟡 Medium"
    else:
        return "🔴 Low"


def get_label_color(score):
    if score > 70:
        return "#22c55e"
    elif score > 40:
        return "#eab308"
    else:
        return "#ef4444"


# Page Config
st.set_page_config(
    page_title="StartupLens AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for aesthetics
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    .main {
        background-color: #0E1117;
        color: #FAFAFA;
        font-family: 'Inter', sans-serif;
    }
    .stProgress .st-bo {
        background-color: #4CAF50;
    }
    .header-title {
        font-size: 3rem;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-value {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        margin-top: -1rem;
    }
    .metric-card {
        padding: 18px;
        border: 1px solid #2A2F3A;
        border-radius: 14px;
        min-height: 210px;
        background: linear-gradient(135deg, #111827 0%, #1a1f2e 100%);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    .viability-ring {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 28px;
        border-radius: 16px;
        background: linear-gradient(135deg, #111827 0%, #1a1f2e 100%);
        border: 1px solid #2A2F3A;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-title">StartupLens AI<br><span style="font-size: 1.5rem; font-weight: 400; color: #aaa;-webkit-text-fill-color: #aaa;">Startup Intelligence Engine</span></div>', unsafe_allow_html=True)

# User Input — pressing Enter triggers the form automatically
with st.form("analysis_form"):
    query = st.text_input(
        "Enter your startup idea:",
        placeholder="e.g., AI-powered personal tutor for organic chemistry",
        key="idea_input",
    )
    submitted = st.form_submit_button("Analyze Idea", use_container_width=True, type="primary")

if submitted and not query.strip():
    st.warning("Please enter a startup idea first!")
    st.stop()

if submitted and query.strip():
    st.divider()

    with st.spinner("Fetching web data and synthesizing context..."):
        # 1. Fetch web data
        raw_docs = fetch_web_data(query)

        # 2. Clean & Chunk individually per document
        all_chunks = []
        for doc in raw_docs:
            if doc and len(doc.strip()) > 10:
                cleaned = clean_text(doc)
                chunks = chunk_text(cleaned, max_words=300)
                all_chunks.extend(chunks)

        chunks = all_chunks

        if not chunks:
            st.error("Could not find relevant data. Please try another idea.")
            st.stop()

    with st.spinner("Generating embeddings and indexing..."):
        # 3. Embeddings
        embeddings = get_embeddings(chunks)

        # 4. Vector DB
        index = create_index(embeddings)

    with st.spinner("Retrieving context & computing viability..."):
        # 5. Retrieve top chunks
        retrieved_chunks = retrieve(query, index, chunks, k=5)
        context = "\n\n".join(retrieved_chunks)

        # ── Extract Dynamic Features ──────────────────────────────
        num_chunks = len(chunks)

        keywords = query.lower().split()
        joined_chunks_lower = " ".join(chunks).lower()
        keyword_freq = sum(joined_chunks_lower.count(kw) for kw in keywords)

        words = joined_chunks_lower.split()
        unique_word_count = len(set(words))

        if num_chunks > 0:
            avg_chunk_length = sum(len(c.split()) for c in chunks) / num_chunks
        else:
            avg_chunk_length = 0.0

        # ── Compute All Scores via new engine ─────────────────────
        scores = compute_all_scores(
            num_chunks=num_chunks,
            keyword_freq=keyword_freq,
            avg_chunk_length=avg_chunk_length,
            unique_word_count=unique_word_count,
            query=query,
        )

        demand_score = scores["demand"]
        idea_strength_score = scores["idea_strength"]
        competition_score = scores["competition"]
        growth_score = scores["growth"]
        monetization_score = scores["monetization"]
        viability_score = scores["viability"]

        # --- DEBUG LOGGING VIA PRINT ---
        print("\n" + "=" * 50)
        print("🚀 STARTUPLENS AI DEBUG LOGS")
        print("=" * 50)
        print(f"Total documents fetched: {len(raw_docs)}")
        print(f"Total chunks created: {num_chunks}")
        print(f"Features: Num Chunks: {num_chunks}, Keyword Freq: {keyword_freq}, "
              f"Avg Length: {avg_chunk_length:.2f}, Unique Words: {unique_word_count}")
        print(f"Scores: {scores}")
        if len(chunks) > 0:
            print(f"Sample Chunk [0]: {chunks[0][:150]}...")
        if len(chunks) > 10:
            print(f"Sample Chunk [10]: {chunks[10][:150]}...")
        print("=" * 50 + "\n")

    with st.spinner("Generating comprehensive market analysis (Groq)..."):
        # 6. Generate Response
        llm_response = generate_response(query, context)

    # ══════════════════════════════════════════════════════════════
    #                     DISPLAY RESULTS
    # ══════════════════════════════════════════════════════════════

    st.success("Analysis Complete!")

    # ── Viability Hero Section ────────────────────────────────────
    v_color = get_label_color(viability_score)
    st.markdown(
        f"""
        <div class="viability-ring" style="text-align:center;">
            <div style="font-size: 0.95rem; text-transform: uppercase; letter-spacing: 2px; color: #9ca3af;">
                Overall Viability
            </div>
            <div style="font-size: 5rem; font-weight: 800; color: {v_color}; line-height: 1.1; margin: 8px 0;">
                {viability_score}
            </div>
            <div style="font-size: 1.1rem; color: {v_color};">
                {get_label(viability_score)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")

    # ── Product Metrics ───────────────────────────────────────────
    product_metrics = [
        ("", "Market Demand", demand_score,
         "Indicates how many people are likely interested in this idea."),
        ("", "Idea Strength", idea_strength_score,
         "Reflects how clear and differentiated your core concept appears."),
        ("", "Competition Level", competition_score,
         "Shows how crowded this space seems based on similar discussions."),
        ("", "Growth Potential", growth_score,
         "Estimates long-term expansion potential from market context."),
        ("", "Monetization Potential", monetization_score,
         "Estimates how easily this idea can convert into revenue."),
    ]

    st.markdown("### Startup Snapshot")
    metric_cols = st.columns(5)
    for col, (icon, title, metric_score, description) in zip(metric_cols, product_metrics):
        label = get_label(metric_score)
        color = get_label_color(metric_score)
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 1.6rem; line-height: 1;">{icon}</div>
                    <div style="margin-top: 8px; font-size: 1rem; font-weight: 700;">{title}</div>
                    <div style="margin-top: 6px; font-size: 1.8rem; font-weight: 800; color: {color};">{metric_score}</div>
                    <div style="margin-top: 4px; font-size: 1.05rem; font-weight: 600;">{label}</div>
                    <div style="margin-top: 8px; font-size: 0.82rem; color: #9ca3af; line-height: 1.35;">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # ── LLM Response ──────────────────────────────────────────────
    st.markdown(llm_response)

    st.divider()

    with st.expander("View Retrieved Context Data"):
        for i, chunk in enumerate(retrieved_chunks):
            st.markdown(f"**Chunk {i+1}:**")
            st.info(chunk)
