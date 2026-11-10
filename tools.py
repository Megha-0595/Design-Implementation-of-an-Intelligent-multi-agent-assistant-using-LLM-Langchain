from langchain.tools import tool 
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os 
from dotenv import load_dotenv

load_dotenv()

def _get_tavily_client():
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return None
    try:
        return TavilyClient(api_key=api_key)
    except Exception:
        return None

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns an overview summary, titles, URLs, and detailed snippets."""
    client = _get_tavily_client()
    if not client:
        return "Search Error: TAVILY_API_KEY is missing or invalid in your .env file. Please provide a valid key from https://tavily.com/"
    try:
        results = client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=True
        )
        out = []
        answer = results.get("answer")
        if answer:
            out.append(f"=== Direct Search Synthesis ===\n{answer}\n")
        
        for idx, r in enumerate(results.get("results", []), 1):
            title = r.get("title", "No Title")
            url = r.get("url", "")
            content = r.get("content", "")
            # Provide generous snippets (up to 1,000 characters)
            snippet = content[:1000].strip() if content else "No snippet available."
            out.append(
                f"Result {idx}:\nTitle: {title}\nURL: {url}\nSnippet: {snippet}\n"
            )
        return "\n----\n".join(out) if out else "No results found for query."
    except Exception as e:
        return f"Search Error ({type(e).__name__}): {str(e)}. Please check your TAVILY_API_KEY in .env."

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading. Uses Tavily extraction first, falling back to direct web scraping."""
    # Attempt 1: Tavily Extract (handles JavaScript, Cloudflare, SPAs, and cleans markdown)
    client = _get_tavily_client()
    if client:
        try:
            extract_res = client.extract(urls=[url], extract_depth="basic", timeout=15)
            for res_item in extract_res.get("results", []):
                raw = res_item.get("raw_content", "")
                if raw and len(raw.strip()) > 150:
                    return raw.strip()[:6000]
        except Exception:
            pass  # Fall back to direct requests

    # Attempt 2: Direct HTTP request with realistic browser headers
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        resp = requests.get(url, timeout=10, headers=headers)
        if resp.status_code != 200:
            return f"Notice: Could not scrape {url} (HTTP status {resp.status_code}). Try another URL from the search results."
        
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "form", "svg"]):
            tag.decompose()
        
        text = soup.get_text(separator=" ", strip=True)
        if len(text) < 150:
            return f"Notice: Extracted very little text from {url} (site may require JavaScript or authentication). Try another URL from the search results."
        
        return text[:6000]
    except Exception as e:
        return f"Could not scrape URL {url}: {str(e)}. Please try another URL from the search results."
