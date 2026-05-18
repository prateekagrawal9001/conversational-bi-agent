from typing import Literal
from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import preprocess_input_node, generate_sql_node, execute_sql_node, format_report_node

def validation_router(state: AgentState) -> Literal["continue_to_execute", "retry_sql_generation", "abort_max_failures"]:
    """Enforces the max 3-iteration self-correction loop constraint for database integrity."""
    if not state["error_message"]:
        return "continue_to_execute"
    
    if state["iterations"] < 3:
        print(f"🔄 Routing back: Attempt {state['iterations']} failed. Initializing self-correction loop.")
        return "retry_sql_generation"
    
    print("🔺 Routing Terminated: Max 3-iteration boundaries reached without resolution.")
    return "abort_max_failures"

# Build and orchestrate the StateGraph
workflow = StateGraph(AgentState)

workflow.add_node("preprocess", preprocess_input_node)
workflow.add_node("generate_sql", generate_sql_node)
workflow.add_node("execute_sql", execute_sql_node)
workflow.add_node("generate_report", format_report_node)

workflow.set_entry_point("preprocess")
workflow.add_edge("preprocess", "generate_sql")
workflow.add_edge("generate_sql", "execute_sql")

workflow.add_conditional_edges(
    "execute_sql",
    validation_router,
    {
        "continue_to_execute": "generate_report",
        "retry_sql_generation": "generate_sql",
        "abort_max_failures": END
    }
)
workflow.add_edge("generate_report", END)

bi_agent_graph = workflow.compile()
