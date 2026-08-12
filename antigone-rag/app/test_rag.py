from rag import ask_question


question = "Why did Antigone bury Polyneices?"


answer, documents = ask_question(question)


print("\n==============================")
print("ANSWER")
print("==============================")

print(answer)


print("\n==============================")
print("SOURCES")
print("==============================")

for doc in documents:

    page = doc.metadata.get("page")

    if page is not None:
        page += 1

    print(f"Page: {page}")