from typing import Literal, TypedDict
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph

MODEL = "qwen3:8b"

model = ChatOllama(model=MODEL, temperature=0)


class RouterState(TypedDict):
    query : str
    query_type : str
    response : str

def demo_basic_routing():

    # node functions
    def classify_query(state : RouterState) -> dict:
        response = model.invoke(
            f"Classify the query as 'question', 'command', or 'statement'. "
            f"Reply with just the word. \n\n{state['query']}"
        )
        return {"query_type" : response.content.lower().strip()}

    def handle_question(state : RouterState) -> dict:
        response = model.invoke(f"Answer this question: {state['query']}")
        return {"response": f"[Answer] {response.content}"} 

    def handle_commend(state: RouterState) -> dict:
        return {"response" : f"[Executing] I'll help you with: {state['query']}"}

    def handle_statement(state : RouterState) -> dict:
        return {"response" : f"[Acknowledged] Thanks for sharing: {state['query']}"}

    def route_by_type(
            state : RouterState,
    ) -> Literal["question", "command", "statement"]:
        qt = state["query_type"]
        if qt == "question":
          return "question"
        elif qt == "command":
          return "command"
        elif qt == "statement":
          return "statement"
        else:
         return "statement"

    # initalize graph
    graph = StateGraph(RouterState)

    # attach nodes
    graph.add_node("classify_query", classify_query)
    graph.add_node("handle_question", handle_question)
    graph.add_node("handle_commend", handle_commend)
    graph.add_node("handle_statement", handle_statement)

    # create edges
    graph.add_edge(START, "classify_query")
    graph.add_conditional_edges(
        "classify_query",
        route_by_type,
        {
            "question" : "handle_question",
            "command" : "handle_commend",
            "statement" : "handle_statement"
        }
    )
    graph.add_edge("handle_question", END)
    graph.add_edge("handle_commend", END)
    graph.add_edge("handle_statement", END)

    # compile graph
    app = graph.compile()

    queries = [
        "What is the capital of France?",
        "Send an email to John",
        "I love programming",
    ]

    for query in queries:
        result = app.invoke({"query" : query})
        print(f"Query: {query}")
        print(f"Type: {result['query_type']}")
        print(f"Response: {result['response']}")
        print("-" * 40)





class QualityState(TypedDict):
    content: str
    quality_score: int
    feedback: str
    final_content: str
    iteration: int


def demo_improve_score():

    # Node 1: Evaluate content quality
    def evaluate_quality(state: QualityState) -> dict:
        response = model.invoke(
            "Rate this content quality from 1-10. "
            "Reply with just the number.\n\n"
            f"Content: {state['content']}"
        )

        try:
            score = int(response.content.strip())
            score = max(1, min(10, score))
        except (ValueError, TypeError):
            score = 5

        return {"quality_score": score}

    # Node 2: Improve content
    def improve_content(state: QualityState) -> dict:
        response = model.invoke(
            "Improve this content to be more engaging and clear. "
            "Preserve its original meaning.\n\n"
            f"{state['content']}"
        )

        return {
            "content": response.content,
            "iteration": state["iteration"] + 1,
        }

    # Node 3: Finalize content
    def finalize_content(state: QualityState) -> dict:
        return {
            "final_content": state["content"],
            "feedback": (
                f"Approved after {state['iteration']} iterations "
                f"with score {state['quality_score']}/10."
            ),
        }

    # Decide whether to improve or finalize
    def should_continue(
        state: QualityState,
    ) -> Literal["improve", "finalize"]:

        if state["quality_score"] >= 7:
            return "finalize"

        if state["iteration"] >= 3:
            return "finalize"

        return "improve"

    # Initialize graph
    graph = StateGraph(QualityState)

    # Register nodes
    graph.add_node("evaluate", evaluate_quality)
    graph.add_node("improve", improve_content)
    graph.add_node("finalize", finalize_content)

    # Define edges
    graph.add_edge(START, "evaluate")

    graph.add_conditional_edges(
        "evaluate",
        should_continue,
        {
            "improve": "improve",
            "finalize": "finalize",
        },
    )

    graph.add_edge("improve", "evaluate")
    graph.add_edge("finalize", END)

    # Compile graph
    app = graph.compile()
    # save as PNG
    png_bytes = app.get_graph().draw_mermaid_png()
    with open("graph_complex.png", "wb") as f:
        f.write(png_bytes)

    # Run workflow
    result = app.invoke({
        "content": (
                "I want to understand the response of world that need to change the determination that cause soffoction"
        ),
        "quality_score": 0,
        "feedback": "",
        "final_content": "",
        "iteration": 0,
    })

    print("Original: AI is cool")
    print(f"Final: {result['final_content'][:200]}")
    print(f"Score: {result['quality_score']}/10")
    print(f"Feedback: {result['feedback']}")


if __name__ == "__main__":
    demo_improve_score()

      
   