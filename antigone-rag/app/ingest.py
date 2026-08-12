from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# pyrefly: ignore [missing-import]
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


BASE_DIR = Path(__file__).resolve().parent.parent

PDF_PATH = BASE_DIR / "data" / "antigone_2.pdf"
VECTORSTORE_PATH = BASE_DIR / "vectorstore"


print("loding doc ")

loder = PyPDFLoader(PDF_PATH)
docs = loder.load()

print(f"Loaded {len(docs)} pages.")

print("splitting doc ")
splittter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splitted_docs = splittter.split_documents(docs)

print(f"Split {len(splitted_docs)} docs into chunks.")

print("Embedding docs ")
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": False},
)

print("creating faiss index ")
vectorstore = FAISS.from_documents(splitted_docs, embedding)

vectorstore.save_local(VECTORSTORE_PATH)

print("====================================")
print("RAG ingestion completed successfully!")
print(f"Pages  : {len(docs)}")
print(f"Chunks : {len(splitted_docs)}")
print(f"Saved  : {VECTORSTORE_PATH}")
print("====================================")
