import pytest
import os
import sys
from app.service.agent_service import create_graph

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_graph_structure():
    graph = create_graph()
    nodes = graph.nodes.keys()
    assert "researcher" in nodes
    assert "analyst" in nodes
    assert "writer" in nodes

def test_full_execution():
    graph = create_graph()
    inputs = {
        "task": "Security test",
        "research_notes": [],
        "report": {},
        "iterations": 0,
        "approved": False
    }
    result = graph.invoke(inputs)
    assert "title" in result["report"]
    assert "executive_summary" in result["report"]
    assert len(result["research_notes"]) > 0
    print("\n✅ Test de ejecución completado con éxito")
