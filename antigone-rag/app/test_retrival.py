from pathlib import Path

# pyrefly: ignore [missing-import]
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

VECTORSTORE_PATH = BASE_DIR / "vectorstore"


# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# Load FAISS
# --------------------------------------------------

vectorstore = FAISS.load_local(
    str(VECTORSTORE_PATH),
    embeddings,
    allow_dangerous_deserialization=True
)


# --------------------------------------------------
# User question
# --------------------------------------------------

question = "Why did Antigone bury Polyneices?"


# --------------------------------------------------
# Search
# --------------------------------------------------

results = vectorstore.similarity_search(
    question,
    k=4
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\n==============================")
print("QUESTION")
print("==============================")
print(question)


print("\n==============================")
print("RETRIEVED CHUNKS")
print("==============================")

for i, doc in enumerate(results, start=1):

    print(f"\n--- Result {i} ---")

    print("Page:", doc.metadata.get("page", "unknown"))

    print("Source:", doc.metadata.get("source", "unknown"))

    print("\nText:")
    print(doc.page_content)