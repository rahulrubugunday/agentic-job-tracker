from langgraph.graph import StateGraph, END
from graph.state import JobState
from graph.nodes import (
    fetch_jobs_node,
    filter_jobs_node,
    analyze_fit_node,
    store_results_node
)

def build_graph():
    graph = StateGraph(JobState)

    graph.add_node("fetch_jobs", fetch_jobs_node)
    graph.add_node("filter_jobs", filter_jobs_node)
    graph.add_node("analyze_fit", analyze_fit_node)
    graph.add_node("store_results", store_results_node)

    graph.set_entry_point("fetch_jobs")
    graph.add_edge("fetch_jobs", "filter_jobs")
    graph.add_edge("filter_jobs", "analyze_fit")
    graph.add_edge("analyze_fit", "store_results")
    graph.add_edge("store_results", END)

    return graph.compile()