from typing import TypedDict , List , Annotated
from langgraph import graph
from langgraph.graph import StateGraph, END
from app.service.llm_factory import get_model
from app.schemas.agent_schema import FinalReport
import operator
from langsmith import Client
from langsmith import traceable

ls_client = Client()

class AgentState(TypedDict):
    task: str
    research_notes: Annotated[list, operator.add]
    report: dict
    iterations: int
    approved: bool

def run_research_logic(task):
    config = {"configurable": {"thread_id": "1"}}
    result = graph.invoke({"task": task}, config=config)
    return result

@traceable(name="Researcher Agent")
def researcher_node(state: AgentState):
    print(f"--- INVESTIGATING: {state['task']} ---")
    llm = get_model()
    prompt = f"You're an expert researcher. Give me 3 hard, real facts about: {state['task']}. Be different from previous notes."
    response = llm.invoke(prompt)
    return {"research_notes": [response.content]}

@traceable(name="Writer Agent")
def writer_node(state: AgentState):
    print(f"--- WRITING REPORT: {state['task']} ---")
    llm = get_model()
    structured_llm = llm.with_structured_output(FinalReport)
    prompt = f"""Create a professional report on '{state['task']}'. 
        Return:
        - key_findings as a comma-separated list
        - sources as a comma-separated list
        Base it on:{state['research_notes'][0]}"""
    response = structured_llm.invoke(prompt)
    report = response.model_dump()
    if isinstance(report["key_findings"], str):
        report["key_findings"] = [x.strip() for x in report["key_findings"].split(",")]
    if isinstance(report["sources"], str):
        report["sources"] = [x.strip() for x in report["sources"].split(",")]
    return {"report": report}

def create_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("writer", writer_node)

    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher","analyst")
    workflow.add_conditional_edges("analyst", should_continue,{"writer": "writer", "researcher": "researcher"})
    workflow.add_edge("writer", END)
    return workflow.compile()

@traceable(name="Analyst Agent")
def analyst_node(state: AgentState):
    print(f"--- ANALYZING REPORT: {state['task']} ---")
    current_iter = state.get("iterations", 0)
    notes_count = len(state.get("research_notes", []))
    is_ready = notes_count >= 3 or current_iter >= 4
    return {"approved": is_ready, "iterations": state['iterations'] + 1}

def should_continue(state: AgentState):
    if state["approved"]:
        return "writer"
    return "researcher"