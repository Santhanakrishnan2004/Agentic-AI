from state import ResearchState


def supervisor_node(state: ResearchState) -> dict:
    """
    Reads current state and decides what to do next.
    Never calls any API — pure logic only.
    """
    print(f"[Supervisor] checking state...")

    if not state.get("search_results"):
        print("[Supervisor] no results yet → search")
        return {"next_step": "search"}

    if not state.get("ranked_results"):
        print("[Supervisor] results found → analyze")
        return {"next_step": "analyze"}

    if not state.get("report"):
        print("[Supervisor] analysis done → write")
        return {"next_step": "write"}

    print("[Supervisor] everything done → done")
    return {"next_step": "done"}
