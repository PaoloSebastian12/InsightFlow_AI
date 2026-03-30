from fastapi import FastAPI , HTTPException
from app.schemas.agent_schema import ResearchRequest, FinalReport
from app.service.llm_factory import get_model
from app.service.agent_service import create_graph

app = FastAPI(title="InsightFlow AI",description="Multi-Agent System for Executive Investigation", version="0.1.0")

graph = create_graph()

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
        result = graph.invoke(initial_state)
        return {"task": request.task,
            "final_report": result["report"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in agent flow: {str(e)}")
