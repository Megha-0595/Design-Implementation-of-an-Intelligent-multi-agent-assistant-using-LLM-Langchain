# 🔬 Multi-Agent Deep Research System (ResearchMind)

An autonomous multi-agent research network powered by **LangChain**, **Streamlit**, and **Tavily**. The system coordinates specialized AI agents that query the live web, bypass paywalls/anti-bot gates to extract primary documents, synthesize exhaustive multi-perspective research reports, and perform rigorous peer-review evaluation in real time.

---

## 🚀 Key Features

* **🔍 Search Agent:** Conducts advanced web queries via Tavily with direct search synthesis and expanded content snippets.
* **📄 Reader Agent:** Intelligent extraction agent utilizing Tavily AI Extract and browser-emulated fallbacks to parse JavaScript SPAs and anti-bot protected sites without failure. Includes dynamic multi-URL fallback.
* **✍️ Writer Chain:** Synthesizes structured, publication-grade research dossiers covering Executive Summary, Comprehensive Deep-Dive Pillars, Real-World Implications, Strategic Roadmaps, and Source Citations.
* **🎯 Critic Chain:** Automated peer-review scoring and critique evaluating technical rigor, factual grounding, and source credibility.
* **💻 Interactive UI:** Streamlit dashboard with real-time status pipelines, KPI telemetry (words synthesized, sources consulted, latency), markdown report exports, and full inspection tabs.

---

## 🛠️ System Architecture

```text
User Topic Input
       │
       ▼
[01: Search Agent] ──▶ Queries Live Web & Aggregates Snippets
       │
       ▼
[02: Reader Agent] ──▶ Extracts Full-Text via Tavily Extract / Scraper
       │
       ▼
[03: Writer Chain] ──▶ Synthesizes Multi-Section In-Depth Report
       │
       ▼
[04: Critic Chain] ──▶ Peer-Review Evaluation & Scoring (X/10)
```

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/<YOUR-USERNAME>/Multi-agent-research-system.git
cd Multi-agent-research-system
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On macOS / Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` and fill in your API credentials:
* **`TAVILY_API_KEY`**: Get a free API key at [tavily.com](https://tavily.com).
* **`GROQ_API_KEY`**: Get a free API key at [console.groq.com](https://console.groq.com) (or use `OPENAI_API_KEY`).

---

## 🖥️ Running the Application

### Option A: Interactive Streamlit Web Dashboard (Recommended)
```bash
streamlit run app.py
```
Or double-click `run_app.bat` on Windows.

### Option B: Terminal CLI Pipeline
```bash
python pipeline.py
```
Or double-click `run_pipeline.bat` on Windows.

---

## 📂 Project Structure

```text
├── agents.py         # Agent definitions, system prompts, Writer & Critic chains
├── app.py            # Streamlit dashboard and UI visualization
├── pipeline.py       # Sequential execution pipeline for CLI use
├── tools.py          # Tavily search and advanced web-scraping tools
├── requirements.txt  # Python package dependencies
├── .env.example      # Example environment configuration
└── README.md         # Project documentation
```

---

## 📄 License
MIT License. Open-source and free to modify for educational and research purposes.
