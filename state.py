# state.py
from typing import TypedDict, Annotated
from operator import add


class ResearchState(TypedDict):
    topic: str
    search_results: Annotated[list, add]
    ranked_results: list
    report: str
    next_step: str
