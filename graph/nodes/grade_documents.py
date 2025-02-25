from typing import Any, Dict

from graph.chains.retrieval_grader import retrieval_grader
from graph.state import GraphState


def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question

    Args:
        state (dict): The current graph state

    Returns:
        Dict[str, Any]: Updated state with:
            - filtered_docs: list of relevant documents
            - results: True if relevant documents found, False otherwise
            - question: original question maintained
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")

    question = state["question"]
    documents = state["documents"]

    filtered_docs = []
    results = False

    for d in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content}
        )
        grade = score.binary_score
        if grade.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            continue

    # Set results to True if we found any relevant documents
    if filtered_docs:
        print("---DECISION: RELEVANT DOCUMENTS FOUND---")
        results = True

    # The final return happens after the loop completes. It processes all documents first, then returns the dictionary
    return {"documents": filtered_docs, "question": question, "results": results}
