import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url

load_dotenv()

# Model setup: Automatically use Groq if GROQ_API_KEY is present to avoid OpenAI 429 quota errors
groq_api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
provider = os.getenv("LLM_PROVIDER", "").lower()

if provider == "groq" or (groq_api_key and not groq_api_key.startswith("your_") and provider != "openai"):
    model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
    llm = ChatOpenAI(
        model=model_name,
        temperature=0,
        base_url="https://api.groq.com/openai/v1",
        api_key=groq_api_key
    )
else:
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    llm = ChatOpenAI(
        model=model_name,
        temperature=0,
        api_key=openai_api_key
    )


# 1st agent: Search Agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=(
            "You are an expert research investigator. Your goal is to search the web for authoritative, "
            "comprehensive, and up-to-date information. Query effectively and gather rich, multi-perspective data "
            "on the assigned topic."
        )
    )


# 2nd agent: Reader Agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt=(
            "You are an expert technical reader and web analyst. Given search results, inspect the URLs "
            "and scrape the top 1-2 most informative and reliable sources using scrape_url. "
            "Extract detailed mechanisms, data points, background facts, and key arguments. "
            "If a URL returns an error, notice, or minimal content, immediately scrape another URL from the list "
            "to guarantee strong research depth."
        )
    )


# 3rd chain: Writer Chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an elite principal research analyst and technical author. "
        "Your mission is to produce authoritative, exhaustive, and impeccably structured research reports. "
        "Never output brief, superficial, or generic summaries. Thoroughly unpack nuances, technical mechanisms, "
        "real-world implications, and data. Provide deep, multi-paragraph coverage for every major section."
    )),
    ("human", """Write an extensive, comprehensive research dossier on the topic below based on the gathered research.

Target Topic: {topic}

Research Gathered:
{research}

Structure the report with the following detailed markdown sections:

# Executive Summary & Context
Provide an in-depth orientation: historical background, significance, core problems solved, and why this topic is critical today.

# Comprehensive Key Findings & Deep Dive
Break down the core insights into multiple substantive, well-explained thematic subsections (at least 3-4 distinct areas). For each finding:
- Explain underlying mechanisms, methodologies, or architectural principles in detail.
- Highlight specific facts, benchmarks, data points, or developments from the gathered research.
- Provide concrete context on how this compares to existing paradigms.

# Real-World Implications & Challenges
Analyze practical adoption hurdles, technical limitations, scalability bottlenecks, economic or ethical trade-offs, and risk factors.

# Future Outlook & Strategic Roadmap
Synthesize where this domain is headed over the next 1-3 years and key milestones to watch.

# Sources & Citations
List all specific source URLs discovered in the research with a brief one-line description of what each contributed.

Maintain a professional, rigorous, and analytical tone throughout. Ensure the report is rich in substance, clarity, and actionable insight."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# 4th chain: Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a rigorous and constructive research critic. Evaluate academic and technical reports strictly."),
    ("human", """Review the research report below and evaluate its depth, rigor, structure, and factual grounding.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()
