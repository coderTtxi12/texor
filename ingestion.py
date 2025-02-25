from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

# from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

# Data
pdf_files = [
    "./assets/el_gato_negro.pdf",
]

# Loading the documents
docs = []
for pdf_path in pdf_files:
    loader = PyPDFLoader(pdf_path)
    docs.extend(loader.load())


docs_list = docs

# Transform
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)

# Split the documents into smaller chunks
doc_splits = text_splitter.split_documents(docs_list)


# Embed and Store, only need to store once, so comment this code once you have uploaded your documents in the vectore store
vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-advanced",
    embedding=OpenAIEmbeddings(),
    persist_directory="./.chroma",
)

# Retrieve
retriever = Chroma(
    collection_name="rag-advanced",
    persist_directory="./.chroma",
    embedding_function=OpenAIEmbeddings(),
).as_retriever()  # Initialize the retriever
