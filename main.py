from dotenv import load_dotenv
from graph.workflow import bi_agent_graph

load_dotenv()

def main():
    print("Starting Conversational Business Intelligence (BI) State Machine...")
    
    sample_input = {
        "user_question": "What is our total revenue from the Electronics category?"
    }
    
    final_output = bi_agent_graph.invoke(sample_input)
    
    print("\n" + "="*60)
    print("FINAL CONVERSATIONAL BI AGENT OUTPUT REPORT")
    print("="*60)
    if "final_report" in final_output:
        print(f"Generated SQL Used: \n{final_output['generated_sql']}\n")
        print(f"Executive Presentation:\n{final_output['final_report']}")
    else:
        print("Pipeline shut down safely. Could not resolve target schema requirements within iteration bounds.")
    print("="*60)

if __name__ == "__main__":
    main()
