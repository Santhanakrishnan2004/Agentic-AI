import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from state import ResearchState

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", google_api_key=os.getenv("GOOGLE_API_KEY")
)


def analyst_node(state: ResearchState) -> dict:
    """
    Receives: state["search_results"] — raw Tavily results
              state["topic"] — the research question
    Does: formats results into text, sends to Gemini,
          asks it to extract key points from best sources
    Returns: {"ranked_results": [string], "next_step": "write"}
    """
    print(f"[Analyst] analyzing {len(state['search_results'])} results")

    results_text = ""
    for i, r in enumerate(state["search_results"]):
        results_text += f"\n--- Source {i+1} ---\n"
        results_text += f"Title: {r.get('title', '')}\n"
        results_text += f"URL: {r.get('url', '')}\n"
        results_text += f"Content: {r.get('content', '')[:600]}\n"

    response = llm.invoke(
        [
            SystemMessage(
                content="""You are a research analyst.
Given search results about a topic, extract the 3 most useful sources.
For each one write 3 bullet points of key facts.
Be factual and concise."""
            ),
            HumanMessage(
                content=f"""
Topic: {state['topic']}

Search results:
{results_text}

Extract the key facts from the best sources.
"""
            ),
        ]
    )

    print(f"[Analyst] extraction done")

    return {"ranked_results": [response.content], "next_step": "write"}
