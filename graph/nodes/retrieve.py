from typing import Any, Dict

from graph.state import GraphState
from ingestion import retriever


def retrieve(state: GraphState) -> Dict[str, Any]:
    print("---RETRIEVE---")
    question = state["question"]

    # Doing semantic search and returning the documents
    documents = retriever.invoke(question)

    # Updating the field of documents in the state
    # and adding the current question
    return {"documents": documents, "question": question}
