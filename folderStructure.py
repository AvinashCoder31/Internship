from pathlib import Path

# Define folders to create
folders = [
    "AI-ML-Internship-Eminds/AgentName_using_LangGraph/data",
    "AI-ML-Internship-Eminds/AgentName_using_LangGraph/database",
    "AI-ML-Internship-Eminds/AgentName_using_LangGraph/src/routers",
    "AI-ML-Internship-Eminds/AgentName_using_LangGraph/src/services",
    
    "AI-ML-Internship-Eminds/notebooks",

    "AI-ML-Internship-Eminds/RAG_App_using_langchain/data",
    "AI-ML-Internship-Eminds/RAG_App_using_langchain/database",
    "AI-ML-Internship-Eminds/RAG_App_using_langchain/src/routers",
    "AI-ML-Internship-Eminds/RAG_App_using_langchain/src/services",

    "AI-ML-Internship-Eminds/RAG_without_framework/data",
    "AI-ML-Internship-Eminds/RAG_without_framework/database",
    "AI-ML-Internship-Eminds/RAG_without_framework/src/routers",
    "AI-ML-Internship-Eminds/RAG_without_framework/src/services",
]

# Define files to create
files = [
    # AgentName_using_LangGraph
    "AI-ML-Internship-Eminds/AgentName_using_LangGraph/src/routers/router.py",
    "AI-ML-Internship-Eminds/AgentName_using_LangGraph/src/services/service1.py",
    "AI-ML-Internship-Eminds/AgentName_using_LangGraph/main.py",
    "AI-ML-Internship-Eminds/AgentName_using_LangGraph/requirements.txt",
    "AI-ML-Internship-Eminds/AgentName_using_LangGraph/README.md",
    "AI-ML-Internship-Eminds/AgentName_using_LangGraph/Dockerfile",

    # Notebooks
    "AI-ML-Internship-Eminds/notebooks/LangGraph_basics.ipynb",
    "AI-ML-Internship-Eminds/notebooks/RAG_using_langchain.ipynb",
    "AI-ML-Internship-Eminds/notebooks/RAG_without_frameworks.ipynb",

    # RAG_App_using_langchain
    "AI-ML-Internship-Eminds/RAG_App_using_langchain/src/routers/router.py",
    "AI-ML-Internship-Eminds/RAG_App_using_langchain/src/services/service1.py",
    "AI-ML-Internship-Eminds/RAG_App_using_langchain/main.py",
    "AI-ML-Internship-Eminds/RAG_App_using_langchain/requirements.txt",
    "AI-ML-Internship-Eminds/RAG_App_using_langchain/README.md",
    "AI-ML-Internship-Eminds/RAG_App_using_langchain/Dockerfile",

    # RAG_without_framework
    "AI-ML-Internship-Eminds/RAG_without_framework/src/routers/router.py",
    "AI-ML-Internship-Eminds/RAG_without_framework/src/services/service1.py",
    "AI-ML-Internship-Eminds/RAG_without_framework/main.py",
    "AI-ML-Internship-Eminds/RAG_without_framework/requirements.txt",
    "AI-ML-Internship-Eminds/RAG_without_framework/README.md",
    "AI-ML-Internship-Eminds/RAG_without_framework/Dockerfile",

    # Top-level README
    "AI-ML-Internship-Eminds/README.md",
]

# Create directories
for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

# Create empty files
for file in files:
    Path(file).touch()

print("Full directory structure with top-level README created successfully.")