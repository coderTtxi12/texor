# Texor

## Deep Document Search

Texor enables anyone to perform a deep search through documents using advanced techniques such as RAG (including Advanced RAG, Corrective RAG, SELF RAG), Reflection Agents, GraphState, and vector stores via Chroma.

## Features

- **Advanced RAG Techniques:** Integrates multiple RAG approaches including Corrective, and SELF RAG.
- **Reflection Agents:** Ensures that generated answers are well-grounded in the provided documents.
- **Graph-Based Workflow:** Uses GraphState to manage the flow of operations.
- **Vector Store with Chroma:** Embeds documents and provides efficient semantic search.
- **Easy Configuration:** Simple setup instructions to ingest documents, specify your query, and run a deep search.

## Graph-Based Workflow

Texor uses a graph-based state management system to process the workflow:

- **Ingestion:** Vector Store with Chroma, embeds documents and provides efficient semantic search. by default the system uses text-embedding-ada-002, Vector Dimensions: 1536.
- **Retrieve:** Fetches relevant documents via semantic search.
- **Grade Documents:** Checks the relevance of retrieved documents.
- **Generate:** Produces an answer based on the relevant documents and the query.
- **Hallucination Grader:** Acts as a reflection agent that evaluates whether the LLM-generated answer is fully supported by the retrieved facts.
- **Grading:** Uses specialized graders to ensure that the generated answer is both grounded in the documents and addresses the question.

## Project Structure

Below is the structure of the project as seen in your environment:

```
.
├── assets/
│   └── el_gato_negro.pdf            # Example PDF for ingestion
├── graph/                           # Core graph components
│   ├── chains/                      # Processing chains
│   │   ├── tests/
│   │   │   └── test_chains.py       # Example test for chain modules
│   │   ├── answer_grader.py
│   │   ├── generation.py
│   │   ├── hallucination_grader.py
│   │   └── retrieval_grader.py
│   └── nodes/                       # Graph nodes
│   │   ├── generate.py
│   │   ├── grade_documents.py
│   │   └── retrieve.py
│   ├── consts.py                    # Constants
│   ├── graph.py                     # Workflow definition
│   └── state.py                     # State management
├── .gitignore
├── ingestion.py                     # Document ingestion, splitting, and vector store creation
├── main.py                          # Entry point for running the app
├── poetry.lock
├── pyproject.toml                   # Poetry configuration file
└── README.md                        # This file
```

## Prerequisites

- [Python 3.8+](https://www.python.org/)
- [Poetry](https://python-poetry.org/) for dependency management

## Setup

1. **Clone the repository:**

```bash
git clone https://github.com/coderTtxi12/texor.git
cd texor
```

2. **Install dependencies using Poetry:**

```bash
poetry install
```

3. **Configure Environment Variables:**

   - Create a .env file in the root directory.
   - Add any necessary environment variables (e.g., OpenAI API keys).

4. **Store your Documents:**

   - Place your documents inside the `/assets` folder.
   - Update `pdf_files` in `ingestion.py` with the path to your documents.

   ```python
   # ingestion.py
   pdf_files = [
       "./assets/el_gato_negro.pdf",
   ]
   ```

5. **Configure Your Query:**

   - Modify the `question` variable in `main.py` with your desired query.

   ```python
   # main.py
   question = "Por qué el libro se llama el gato negro? justifica tu respuesta"
   ```

## Running the Project

Run the main application:

```bash
poetry run python main.py
```

The system will invoke the agentic workflow and provide a deep search answer based on the ingested documents.

## Overview

- **Document Retrieval:** The system retrieves related documents based on your query.
- **Document Grading:** Relevance of documents is evaluated to filter for the best matches.
- **Generation:** If relevant documents are found, an answer is generated and evaluated.

Explore the source code and experiment with different queries to leverage the full potential of Texor.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests if you have suggestions or improvements.

## License
MIT License
