from langgraph.graph import StateGraph, END
from .state import HealthState
from .nodes import analyze_node, recommendation_node


def build_health_workflow():
    workflow = StateGraph(HealthState)

    workflow.add_node("analyze", analyze_node)
    workflow.add_node("recommend", recommendation_node)

    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "recommend")
    workflow.add_edge("recommend", END)

    return workflow.compile()