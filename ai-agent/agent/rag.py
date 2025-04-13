# --- agent/rag.py ---
import bs4
from langchain import hub
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph, END
from typing import List, TypedDict
from langchain_core.prompts import ChatPromptTemplate

from agent.llm import llm 
from db.vectorstore import vector_store 

# --- State Definition ---
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str



prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant answering questions based on context."),
    # Note: The "add more knowledge" part is hardcoded here.
    ("user", "Answer the question based on the following context:\n\n{context}\n\nQuestion: {question} and also add more knowledge to the answer if possible."),
])

# --- Nodes ---
def retrieve(state: State):
    """Retrieves documents relevant to the question."""
    print(f"[retrieve] Retrieving documents for question: {state['question']}")
    try:
        # Use the globally accessible vector_store
        retrieved_docs = vector_store.similarity_search(state["question"])
        print(f"[retrieve] Found {len(retrieved_docs)} documents.")
        return {"context": retrieved_docs}
    except Exception as e:
        print(f"[retrieve] Error during similarity search: {e}")
        return {"context": []}


def generate(state: State):
    """Generates an answer using the LLM based on retrieved context."""
    print(f"[generate] Generating answer for question: {state['question']}")
    print(f"[generate] Context length: {len(state['context'])}")
    question = state["question"]
    context_docs = state["context"]

    if not context_docs:
        print("[generate] Warning: No context found, generating answer based on question only.")
        docs_content = "No specific context found."
        # return {"answer": "I couldn't find relevant information in the provided documents to answer your question."}

    else:
        docs_content = "\n\n".join(doc.page_content for doc in context_docs)

    messages = prompt.invoke({"question": question, "context": docs_content})
    print(f"[generate] Prompt messages: {messages}") # Log the actual prompt sent

    try:
        response = llm.invoke(messages, config={"configurable": {"callbacks": True}})

        print(f"[generate] LLM response content: {response.content}")
        return {"answer": response.content}
    except Exception as e:
        print(f"[generate] Error during LLM invocation: {e}")
        # Decide how to handle LLM errors
        return {"answer": f"Sorry, an error occurred while generating the answer: {e}"}


# --- Graph Definition ---
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("retrieve", retrieve)
graph_builder.add_node("generate", generate)

# Define edges
graph_builder.add_edge(START, "retrieve") # Start with retrieval
graph_builder.add_edge("retrieve", "generate") # Move from retrieval to generation
graph_builder.add_edge("generate", END) # End after generation

# Compile the graph
graph = graph_builder.compile()

print("RAG graph compiled successfully.")

# Remove the redundant document loading/processing from this file
# docs = text_loader("./uploaded_files/main.txt")
# text_splitter = ...
# all_splits = ...
# texts = ...
# _=vector_store.add_texts(...)