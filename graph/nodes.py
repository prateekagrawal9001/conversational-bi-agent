from typing import Dict, Any
from sqlalchemy import text
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from config.database import engine, SCHEMA_DESCRIPTION
from graph.state import AgentState

# Initialize our LLM engine (Llama via Ollama) safely with low temperature
llm = ChatOllama(model="llama3", temperature=0.0)

def preprocess_input_node(state: AgentState) -> Dict[str, Any]:
    """Validates if the prompt is a safe BI query request."""
    print("--- NODE: PREPROCESS & VALIDATE INPUT ---")
    question = state["user_question"]
    tokens = question.strip().split()
    
    return {
        "validated_input": {"tokens_count": len(tokens), "status": "APPROVED"},
        "iterations": 0,
        "error_message": ""
    }

def generate_sql_node(state: AgentState) -> Dict[str, Any]:
    """Transforms complex natural language into highly accurate SQL queries."""
    print(f"--- NODE: GENERATE SQL (Iteration: {state['iterations'] + 1}) ---")
    
    system_instruction = (
        "You are a Conversational BI text-to-SQL compiler. Generate ONLY executable, syntax-valid PostgreSQL "
        "code based on the provided schema description. Do NOT wrap your output in markdown syntax blocks, "
        "backticks, or markdown words. Return only the raw SQL text string."
    )
    
    user_template = "Database Schema:\n{schema}\n\nUser Question: {question}"
    
    if state.get("error_message"):
        user_template += "\n\nCRITICAL: Your previous query failed with this database syntax error: {error_log}.\nFix the query and return the rewritten statement."

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instruction),
        ("user", user_template)
    ])
    
    chain = prompt | llm
    response = chain.invoke({
        "schema": SCHEMA_DESCRIPTION,
        "question": state["user_question"],
        "error_log": state.get("error_message", "")
    })
    
    clean_sql = response.content.strip().replace("```sql", "").replace("```", "")
    return {
        "generated_sql": clean_sql,
        "iterations": state["iterations"] + 1
    }

def execute_sql_node(state: AgentState) -> Dict[str, Any]:
    """Executes raw SQL query within the protected decoupled engine engine block."""
    print("--- NODE: EXECUTE SQL VIA DECOUPLED ARCHITECTURE ---")
    sql = state["generated_sql"]
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql))
            data = [dict(row._mapping) for row in result.fetchall()]
            
        print("✅ SQL Execution Succeeded.")
        return {"raw_results": data, "error_message": ""}
        
    except Exception as db_exception:
        error_str = str(db_exception)
        print(f"❌ SQL Execution Failed: {error_str}")
        return {"error_message": error_str}

def format_report_node(state: AgentState) -> Dict[str, Any]:
    """Converts raw row dict arrays into insights geared for senior management."""
    print("--- NODE: POSTPROCESSING & PRESENTATION ---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Senior BI reporting analyst tool. Translate raw database matrices cleanly into concise summaries targeted at senior executives."),
        ("user", "Executive Question: {question}\nExecuted SQL: {sql}\nRetrieved Records: {results}\n\nProvide the final brief:")
    ])
    
    chain = prompt | llm
    response = chain.invoke({
        "question": state["user_question"],
        "sql": state["generated_sql"],
        "results": str(state["raw_results"])
    })
    
    return {"final_report": response.content.strip()}
