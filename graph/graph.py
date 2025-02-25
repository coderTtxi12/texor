from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

# from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph

from graph.chains.answer_grader import answer_grader
from graph.chains.hallucination_grader import hallucination_grader
from graph.consts import GENERATE, GRADE_DOCUMENTS, RETRIEVE
from graph.nodes import generate, grade_documents, retrieve
from graph.state import GraphState

load_dotenv()


def decide_to_generate(state):
    print("---ASSESS GRADED DOCUMENTS---")

    if state["results"]:
        print("---DECISION: RELEVANT DOCUMENTS FOUND THEN LET'S GENERATE---")
        return GENERATE
    else:
        print("---DECISION: NO RELEVANT DOCUMENTS FOUND---")
        return END


def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:

    print("---CHECK HALLUCINATIONS---")

    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )

    if hallucination_grade := score.binary_score:

        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        print("---GRADE GENERATION vs QUESTION---")

        score = answer_grader.invoke({"question": question, "generation": generation})
        if answer_grade := score.binary_score:
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not answerable"


# Initialize the graph
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)

# Entry point
workflow.set_entry_point(RETRIEVE)

# Add edges
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)


workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    {
        GENERATE: GENERATE,
        END: END,
    },
)


workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    {
        "not supported": GENERATE,
        "useful": END,
        "not answerable": GENERATE,
    },
)


app = workflow.compile()

# app.get_graph().draw_mermaid_png(output_file_path="graph.png")
