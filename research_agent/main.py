import os
import uuid
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from graph import graph

load_dotenv()

app = FastAPI()


class ResearchRequest(BaseModel):
    topic: str
    thread_id: str = None


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/research")
def run_research(request: ResearchRequest):
    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    result = graph.invoke(
        {
            "topic": request.topic,
            "search_results": [],
            "ranked_results": [],
            "report": "",
            "next_step": "",
        },
        config=config,
    )

    return {"thread_id": thread_id, "topic": request.topic, "report": result["report"]}


@app.post("/research/stream")
async def stream_research(request: ResearchRequest):
    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    def generate():
        for event in graph.stream(
            {
                "topic": request.topic,
                "search_results": [],
                "ranked_results": [],
                "report": "",
                "next_step": "",
            },
            config=config,
            stream_mode="updates",
        ):
            node_name = list(event.keys())[0]
            node_output = event[node_name]

            if node_name == "writer" and "report" in node_output:
                report = node_output["report"]
                chunk_size = 50
                for i in range(0, len(report), chunk_size):
                    chunk = report[i : i + chunk_size]
                    yield f"data: {chunk}\n\n"
            else:
                yield f"data: [STATUS:{node_name}]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
