# Conversational Business Intelligence (BI) Agent

A production-ready Text-to-SQL state-machine orchestrator built using LangGraph, LangChain, and Gemini 1.5 Pro.

## Features
- **Decoupled Architecture**: Interacts safely with database layers using decoupled metadata schema logic via SQLAlchemy.
- **Self-Correction Pipeline**: Implements an automated loop structure bounded strictly to a max of 3 retry iterations on database exceptions.
- **Input Preprocessing**: Basic tokenization and processing sanitization layers before passing query flows down the graph execution nodes.

## Setup Instructions
1. Clone this repository.
2. Install requirements: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your variables.
4. Run the program execution: `python main.py`