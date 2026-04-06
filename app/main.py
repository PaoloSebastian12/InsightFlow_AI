from pdb import run
from fastapi import FastAPI , HTTPException
from app.schemas.agent_schema import ResearchRequest
from app.service.llm_factory import get_model
from app.service.agent_service import create_graph
from langchain_core.tracers.context import collect_runs
from langsmith import Client

app = FastAPI(title="InsightFlow AI",description="Multi-Agent System for Executive Investigation", version="0.1.0")
client = Client()
graph = create_graph()

#limitacao de gemini entao se faz uma aproximacao de tokens
def estimate_tokens(text: str):
    return int(len(text.split()) * 1.3)

@app.get("/")
async def read_root():
    return {"status": "online", "project": "InsightFlow AI"}
    
@app.post("/research")
async def run_research(request: ResearchRequest):
    try:
        initial_state = {
            "task": request.task,
            "research_notes": [],
            "report": "",
            "iterations": 0
        }
        with collect_runs() as cb:
            result = graph.invoke(initial_state)
            total_tokens = 0
            for note in result.get("research_notes", []):
                total_tokens += estimate_tokens(note)
            report = result.get("report", {})
            if isinstance(report, dict):
                for value in report.values():
                    if isinstance(value, str):
                        total_tokens += estimate_tokens(value)
                    elif isinstance(value, list):
                        for item in value:
                            total_tokens += estimate_tokens(str(item))
            if cb.traced_runs:
                run_id = str(cb.traced_runs[0].id)
            else:
                run_id = "no_id_found"
            latency = 0
            if run_id != "no_id_found":
                try:
                    run_data = client.read_run(run_id)
                    if run_data.end_time and run_data.start_time:
                        latency = (run_data.end_time - run_data.start_time).total_seconds()
                except Exception as e:
                    print("LangSmith fetch error:", e)
                    latency = 0
        return {
            "task": request.task,
            "final_report": result["report"],
            "trace_id": run_id,
            "usage": {"total_tokens": total_tokens}, 
            "latency": latency
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in agent flow: {str(e)}")
