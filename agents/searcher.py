import os
from dotenv import load_dotenv
from tavily import TavilyClient
from state import ResearchState

load_dotenv()


def searcher_node(state: ResearchState) -> dict:
    """
    Receives: state["topic"]
    Does: calls Tavily search API with that topic
    Returns: {"search_results": [list of result dicts], "next_step": "analyze"}

    Each result dict from Tavily has these keys:
        title   → headline of the page
        url     → source link
        content → extracted text snippet
        score   → relevance score (0 to 1)
    """
    print(f"[Searcher] searching for: {state['topic']}")

    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    response = client.search(query=state["topic"], max_results=5)

    results = response.get("results", [])

    print(f"[Searcher] got {len(results)} results")

    return {"search_results": results, "next_step": "analyze"}
