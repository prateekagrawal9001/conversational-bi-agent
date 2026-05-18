from typing import Dict, Any, TypedDict

class AgentState(TypedDict):
    user_question: str
    validated_input: Dict[str, Any]
    generated_sql: str
    error_message: str
    iterations: int
    raw_results: list
    final_report: str
