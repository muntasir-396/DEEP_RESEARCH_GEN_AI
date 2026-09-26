from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


# --------------------------------------------------
# 1. Embedding Model
# --------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# 2. Text Splitter
# --------------------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)


# --------------------------------------------------
# 3. Create Vector Database
# --------------------------------------------------

def create_vector_store(documents):

    chunks = text_splitter.split_documents(documents)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    return vector_store


# --------------------------------------------------
# 4. Retrieve Relevant Documents
# --------------------------------------------------

def retrieve_documents(vector_store, query, k=5):

    retriever = vector_store.as_retriever(
        search_kwargs={"k": k}
    )

    documents = retriever.invoke(query)

    return documents