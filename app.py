import streamlit as st
import time
import re
import os
from dotenv import load_dotenv
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

load_dotenv()

# ── 1. Page Configuration ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI · Autonomous Deep Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── 2. Production-Grade Modern Design System (CSS) ────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* ── Global Theme Reset ── */
:root {
    --bg-page: #0b0f17;
    --card-bg: #111827;
    --card-border: rgba(255, 255, 255, 0.08);
    --card-border-hover: rgba(99, 102, 241, 0.4);
    --primary: #4f46e5;
    --primary-gradient: linear-gradient(135deg, #6366f1 0%, #3b82f6 50%, #06b6d4 100%);
    --text-heading: #ffffff;
    --text-body: #e2e8f0;
    --text-muted: #94a3b8;
    --emerald: #10b981;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-body);
}

.stApp {
    background-color: var(--bg-page);
    background-image: 
        radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.12) 0%, transparent 50%),
        radial-gradient(circle at 90% 90%, rgba(6, 182, 212, 0.06) 0%, transparent 40%);
    background-attachment: fixed;
}

/* ── Hide Streamlit Default Chrome ── */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
    padding: 1.8rem 2.5rem 4rem !important;
    max-width: 1200px;
    margin: 0 auto;
}
xs
/* ── Top Header Navigation ── */
.nav-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--card-border);
    margin-bottom: 2.5rem;
}
.brand-box {
    display: flex;
    align-items: center;
    gap: 0.85rem;
}
.brand-logo {
    background: var(--primary-gradient);
    width: 42px;
    height: 42px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
}
.brand-name {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #ffffff;
}
.brand-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.25);
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    margin-left: 0.5rem;
}

/* ── Hero Headline ── */
.hero-box {
    text-align: center;
    margin-bottom: 2.2rem;
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    color: #a5b4fc;
    background: rgba(99, 102, 241, 0.14);
    border: 1px solid rgba(99, 102, 241, 0.3);
    padding: 0.3rem 0.9rem;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 1rem;
}
.hero-headline {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(2.3rem, 4.5vw, 3.4rem);
    font-weight: 800;
    color: #ffffff;
    line-height: 1.15;
    letter-spacing: -0.03em;
    margin: 0 0 0.8rem;
}
.hero-gradient-text {
    background: linear-gradient(135deg, #818cf8 0%, #38bdf8 60%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-description {
    font-size: 1.05rem;
    color: var(--text-muted);
    max-width: 640px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Native Streamlit Bordered Container Customization ── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #111827 !important;
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    border-radius: 16px !important;
    padding: 1.5rem 1.8rem !important;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5) !important;
}

/* ── Text Input Styling ── */
.stTextInput > div > div > input {
    background: #0b1120 !important;
    border: 1.5px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-size: 1.05rem !important;
    padding: 0.85rem 1.15rem !important;
    transition: all 0.2s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
}
.stTextInput > label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    color: #f1f5f9 !important;
    margin-bottom: 0.4rem !important;
}

/* ── Primary Action Button ── */
.stButton > button {
    background: var(--primary-gradient) !important;
    color: #ffffff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.98rem !important;
    letter-spacing: 0.01em !important;
    border: none !important;
    border-radius: 11px !important;
    padding: 0.75rem 1.8rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.5) !important;
    filter: brightness(1.08) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Prompt Pill Buttons ── */
.pill-row div[data-testid="stButton"] > button {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #cbd5e1 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.4rem 0.85rem !important;
    border-radius: 9999px !important;
    box-shadow: none !important;
    transition: all 0.15s ease !important;
}
.pill-row div[data-testid="stButton"] > button:hover {
    background: rgba(99, 102, 241, 0.2) !important;
    border-color: rgba(99, 102, 241, 0.5) !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
}

/* ── Agent Pipeline Stage Cards ── */
.stage-card {
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 1.15rem 1.25rem;
    transition: all 0.2s ease;
    height: 100%;
}
.stage-card:hover {
    border-color: rgba(255, 255, 255, 0.18);
}
.stage-card.active {
    border-color: rgba(56, 189, 248, 0.55);
    background: rgba(14, 165, 233, 0.07);
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.18);
}
.stage-card.completed {
    border-color: rgba(16, 185, 129, 0.45);
    background: rgba(16, 185, 129, 0.05);
}
.stage-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.6rem;
}
.stage-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    color: #818cf8;
}
.stage-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    font-weight: 700;
    padding: 0.18rem 0.55rem;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.pill-idle      { background: rgba(148, 163, 184, 0.12); color: #94a3b8; }
.pill-active    { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.35); }
.pill-completed { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35); }

.stage-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.25rem;
}
.stage-desc {
    font-size: 0.8rem;
    color: var(--text-muted);
    line-height: 1.4;
}

/* ── KPI Metric Cards ── */
.kpi-card {
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
}
.kpi-value {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.75rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
    margin-bottom: 0.25rem;
}
.kpi-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Tabs Customization ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: rgba(15, 23, 42, 0.6);
    border-radius: 12px;
    padding: 0.35rem;
    border: 1px solid rgba(255, 255, 255, 0.08);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important;
    padding: 0.55rem 1.25rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    color: #94a3b8 !important;
    border: none !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(99, 102, 241, 0.22) !important;
    color: #ffffff !important;
    border: 1px solid rgba(99, 102, 241, 0.4) !important;
}

/* ── Report Reading Container ── */
.report-body {
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 2.2rem 2.6rem;
    line-height: 1.85;
    font-size: 1rem;
    color: #f1f5f9;
}
.report-body h1, .report-body h2, .report-body h3 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #ffffff;
    letter-spacing: -0.02em;
    margin-top: 1.4rem;
}

/* ── Critic Score Box ── */
.critic-review-box {
    background: #111827;
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 16px;
    padding: 2rem 2.4rem;
}
.critic-top-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.score-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.2rem;
    font-weight: 700;
    padding: 0.35rem 1rem;
    border-radius: 10px;
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.35);
}
</style>
""", unsafe_allow_html=True)


# ── 3. Session State Initialization ───────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = {}
if "running" not in st.session_state:
    st.session_state.running = False
if "done" not in st.session_state:
    st.session_state.done = False
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "duration" not in st.session_state:
    st.session_state.duration = 0.0


# ── 4. Clean Top Header Navigation ────────────────────────────────────────────
nav_col1, nav_col2 = st.columns([8, 2])
with nav_col1:
    st.markdown("""
    <div class="nav-header" style="margin-bottom:0;padding-bottom:0.5rem;border-bottom:none;">
        <div class="brand-box">
            <div class="brand-logo">🔬</div>
            <div>
                <span class="brand-name">ResearchMind</span>
                <span class="brand-badge">Deep Research v2.0</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with nav_col2:
    if st.button("🔄 New Research", use_container_width=True):
        st.session_state.results = {}
        st.session_state.running = False
        st.session_state.done = False
        st.session_state.topic_input = ""
        st.rerun()

st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.08);margin:0.8rem 0 2rem;'>", unsafe_allow_html=True)


# ── 5. Hero Headline ─────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
    <div class="hero-tag">
        <span>⚡</span> Autonomous Intelligence Network
    </div>
    <h1 class="hero-headline">
        Autonomous <span class="hero-gradient-text">Deep Research</span> Engine
    </h1>
    <p class="hero-description">
        Coordinate specialized AI agents that browse the live web, extract primary literature, 
        synthesize structured findings, and conduct peer-review evaluation in real-time.
    </p>
</div>
""", unsafe_allow_html=True)


# ── 6. Research Console (Native Streamlit Container) ──────────────────────────
with st.container(border=True):
    topic = st.text_input(
        "Enter Target Research Topic or Inquiry",
        value=st.session_state.topic_input,
        placeholder="e.g., Autonomous LLM reasoning and self-correcting agents in 2026",
        key="main_topic_field"
    )
    st.session_state.topic_input = topic

    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
    launch_btn = st.button("🚀 Start Deep Research", use_container_width=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown("<span style='font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#94a3b8;letter-spacing:0.06em;'>TRY EXAMPLES:</span>", unsafe_allow_html=True)

    st.markdown('<div class="pill-row">', unsafe_allow_html=True)
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        if st.button("🔬 Autonomous AI Agents", key="pill_1", use_container_width=True):
            st.session_state.topic_input = "Autonomous LLM reasoning and self-correcting agents in 2026"
            st.rerun()
    with col_p2:
        if st.button("🧬 In-Vivo CRISPR Prime", key="pill_2", use_container_width=True):
            st.session_state.topic_input = "Latest breakthroughs in in-vivo CRISPR prime editing"
            st.rerun()
    with col_p3:
        if st.button("⚡ Solid-State Electrolytes", key="pill_3", use_container_width=True):
            st.session_state.topic_input = "Commercial viability of solid-state battery electrolytes 2026"
            st.rerun()
    with col_p4:
        if st.button("🌐 Room-Temp Superconductors", key="pill_4", use_container_width=True):
            st.session_state.topic_input = "Current state of room-temperature superconductor research"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)


# ── 7. Clean 4-Column Horizontal Pipeline Visualizer ──────────────────────────
res = st.session_state.results
is_running = st.session_state.running

def get_stage_state(step_key: str):
    if not res and not is_running:
        return ("idle", "pill-idle", "STANDBY")
    if step_key in res:
        return ("completed", "pill-completed", "COMPLETED")
    if is_running:
        steps = ["search", "reader", "writer", "critic"]
        for s in steps:
            if s not in res:
                return ("active", "pill-active", "WORKING") if s == step_key else ("idle", "pill-idle", "WAITING")
    return ("idle", "pill-idle", "STANDBY")

def render_stage_card(num: str, icon: str, name: str, desc: str, step_key: str):
    state_cls, pill_cls, label = get_stage_state(step_key)
    st.markdown(f"""
    <div class="stage-card {state_cls}">
        <div class="stage-top">
            <span class="stage-num">{num}</span>
            <span class="stage-pill {pill_cls}">{label}</span>
        </div>
        <div class="stage-title">{icon} {name}</div>
        <div class="stage-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

pipe_col1, pipe_col2, pipe_col3, pipe_col4 = st.columns(4)
with pipe_col1:
    render_stage_card("01", "🔍", "Search Agent",  "Gathers recent web articles & source URLs", "search")
with pipe_col2:
    render_stage_card("02", "📄", "Reader Agent",  "Scrapes primary text and isolates key data", "reader")
with pipe_col3:
    render_stage_card("03", "✍️", "Writer Chain",  "Synthesizes structured findings into a report", "writer")
with pipe_col4:
    render_stage_card("04", "🎯", "Critic Chain",  "Evaluates rigor, sources, and grades report", "critic")


# ── 8. Execution Pipeline Loop ────────────────────────────────────────────────
if launch_btn:
    current_topic = st.session_state.topic_input.strip()
    if not current_topic:
        st.warning("Please enter a research topic to proceed.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.session_state.start_time = time.time()
        st.rerun()

if st.session_state.running and not st.session_state.done:
    target_topic = st.session_state.topic_input.strip()
    pipeline_state = {}

    try:
        # Step 1: Search Agent
        with st.spinner("🔍 Step 1 of 4: Search Agent querying live web intelligence..."):
            search_agent = build_search_agent()
            search_res = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {target_topic}")]
            })
            pipeline_state["search"] = search_res["messages"][-1].content
            st.session_state.results["search"] = pipeline_state["search"]

        # Step 2: Reader Agent
        with st.spinner("📄 Step 2 of 4: Reader Agent scraping and analyzing top sources..."):
            reader_agent = build_reader_agent()
            reader_res = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{target_topic}', "
                    f"pick the top 1-2 most informative URLs and scrape them for deep content. "
                    f"If one URL fails or has minimal text, scrape another URL from the list.\n\n"
                    f"Search Results:\n{pipeline_state['search']}"
                )]
            })
            pipeline_state["reader"] = reader_res["messages"][-1].content
            st.session_state.results["reader"] = pipeline_state["reader"]

        # Step 3: Writer Chain
        with st.spinner("✍️ Step 3 of 4: Writer Chain synthesizing research dossier..."):
            research_combined = (
                f"SEARCH RESULTS:\n{pipeline_state['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{pipeline_state['reader']}"
            )
            pipeline_state["writer"] = writer_chain.invoke({
                "topic": target_topic,
                "research": research_combined
            })
            st.session_state.results["writer"] = pipeline_state["writer"]

        # Step 4: Critic Chain
        with st.spinner("🎯 Step 4 of 4: Critic Chain conducting peer-review evaluation..."):
            pipeline_state["critic"] = critic_chain.invoke({
                "report": pipeline_state["writer"]
            })
            st.session_state.results["critic"] = pipeline_state["critic"]

        st.session_state.duration = round(time.time() - st.session_state.start_time, 1)
        st.session_state.running = False
        st.session_state.done = True
        st.rerun()

    except Exception as e:
        st.session_state.running = False
        st.error(f"**Pipeline Error Occurred:** {str(e)}")
        st.info("Tip: Check your API keys in `.env` or network connectivity.")


# ── 9. Real Production Results Dashboard ──────────────────────────────────────
res_data = st.session_state.results

if res_data and "writer" in res_data:
    st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.08);margin:2.5rem 0 2rem;'>", unsafe_allow_html=True)
    
    st.success(f"✨ **Research Protocol Completed Successfully** in **{st.session_state.duration} seconds** across 4 autonomous agents.")

    report_text = res_data.get("writer", "")
    critic_text = res_data.get("critic", "")
    word_count = len(report_text.split())
    
    found_urls = re.findall(r'https?://[^\s)\]]+', report_text + res_data.get("search", ""))
    unique_urls = list(set(found_urls))

    score_match = re.search(r'Score:\s*([0-9]+(?:\.[0-9]+)?\s*/\s*10)', critic_text, re.IGNORECASE)
    critic_score = score_match.group(1) if score_match else "Verified"

    # KPI Stat Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{word_count:,}</div>
            <div class="kpi-label">Words Synthesized</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color:#38bdf8;">{len(unique_urls)}</div>
            <div class="kpi-label">Sources Consulted</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color:#34d399;">{critic_score}</div>
            <div class="kpi-label">Critic Score</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color:#818cf8;">{st.session_state.duration}s</div>
            <div class="kpi-label">Total Latency</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Clean Tabs
    tab_report, tab_critic, tab_search, tab_reader = st.tabs([
        "📑 Final Research Dossier",
        "🎯 Critic Evaluation",
        "🔍 Search Intelligence",
        "📄 Raw Source Text"
    ])

    with tab_report:
        col_hdr, col_btn = st.columns([7.5, 2.5])
        with col_hdr:
            st.markdown("<h3 style='margin:0;font-family:Plus Jakarta Sans;color:#ffffff;'>Executive Research Report</h3>", unsafe_allow_html=True)
        with col_btn:
            st.download_button(
                label="⬇ Download Report (.md)",
                data=report_text,
                file_name=f"research_report_{int(time.time())}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown(report_text)

    with tab_critic:
        with st.container(border=True):
            col_c1, col_c2 = st.columns([8, 2])
            with col_c1:
                st.markdown("<h3 style='margin:0;font-family:Plus Jakarta Sans;color:#ffffff;'>Peer-Review Evaluation</h3><div style='font-size:0.85rem;color:#94a3b8;margin-top:0.2rem;'>Objective report review performed by Critic Chain</div>", unsafe_allow_html=True)
            with col_c2:
                st.markdown(f"<div class='score-badge' style='text-align:center;'>⭐ {critic_score}</div>", unsafe_allow_html=True)
            st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.08);margin:1rem 0;'>", unsafe_allow_html=True)
            st.markdown(critic_text)

    with tab_search:
        st.markdown("<h4 style='color:#ffffff;font-family:Plus Jakarta Sans;margin-bottom:0.75rem;'>Live Tavily Search Results</h4>", unsafe_allow_html=True)
        search_content = res_data.get("search", "No search data available.")
        with st.container(border=True):
            st.code(search_content, language="markdown")

    with tab_reader:
        st.markdown("<h4 style='color:#ffffff;font-family:Plus Jakarta Sans;margin-bottom:0.75rem;'>Extracted Primary Document</h4>", unsafe_allow_html=True)
        scraped_content = res_data.get("reader", "No scraped data available.")
        with st.container(border=True):
            st.text_area("Extracted Full-Text Content", scraped_content, height=450, disabled=True, label_visibility="collapsed")

st.markdown("""
<div style="text-align:center;padding:3rem 0 1.5rem;font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#64748b;">
    RESEARCHMIND AI PLATFORM · MULTI-AGENT ARCHITECTURE
</div>
""", unsafe_allow_html=True)