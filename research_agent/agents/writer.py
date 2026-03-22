import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from state import ResearchState

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", google_api_key=os.getenv("GOOGLE_API_KEY")
)


def writer_node(state: ResearchState) -> dict:
    """
    Receives: state["ranked_results"] — analyst's extracted key points
              state["topic"] — the research question
    Does: sends key points to Gemini, asks for a full markdown report
    Returns: {"report": "...", "next_step": "done"}
    """
    print(f"[Writer] writing report on: {state['topic']}")

    insights = "\n".join(state["ranked_results"])

    response = llm.invoke(
        [
            SystemMessage(
                content="""You are a professional research writer.
Write clear well structured research reports using markdown.
Always include these four sections:
## Summary
## Key Findings
## Analysis
## Conclusion
Be thorough but concise."""
            ),
            HumanMessage(
                content=f"""
Write a research report on: {state['topic']}

Based on these key points extracted from sources:
{insights}
"""
            ),
        ]
    )

    print(f"[Writer] report done — {len(response.content)} characters")

    return {"report": response.content, "next_step": "done"}
