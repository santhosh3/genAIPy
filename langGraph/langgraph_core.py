import operator
from typing import Annotated, TypedDict
from langchain_classic.chat_models import init_chat_model
from langchain_classic.schema import AIMessage, BaseMessage, HumanMessage, StrOutputParser
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph, add_messages

MODEL = 'qwen3:8b'

class SimpleState(TypedDict):
    input: str
    output: str
    step: int

def demo_simple_graph():
    # define node functions
    def process(state : SimpleState) -> dict:
        return {"output" : state["input"].upper(), "step" : state["step"] + 1}

    # create graph
    graph = StateGraph(SimpleState)

    # add nodes
    graph.add_node("process",process)

    # add edges
    graph.add_edge(START, "process")
    graph.add_edge("process", END)

    # compile
    app = graph.compile()

    result = app.invoke({"input" : "hello", "output" : "", "step" : 0})

    print("simple graph result:", result)
    print(
        f" Input: {result['input']}, Output: {result['output']}, Step: {result['step']}"
    )


class AccumulatingState(TypedDict):
    message: Annotated[list[str], operator.add]
    count: Annotated[int, operator.add]

def demo_accumulating_state():
    # define node functions
    def step_one(state : AccumulatingState) -> dict:
        return {"message" : ["step 1 executed"], "count" : 1}

    def step_two(state : AccumulatingState) -> dict:
        return {"message" : ["step 2 executed"], "count" : 1}

    # create graph
    graph = StateGraph(AccumulatingState)

    # add nodes
    graph.add_node("step_one", step_one)
    graph.add_node("step_two", step_two)

    # add edges
    graph.add_edge(START, "step_one")
    graph.add_edge("step_one", "step_two")
    graph.add_edge("step_two", END)

    # compile
    app = graph.compile()

    result = app.invoke({"messages": ["Initial message"], "count": 0})

    print(f"  Messages: {result['message']}")
    print(f"  Count: {result['count']}")

class MessageState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def demo_message_state():
    llm = ChatOllama(model=MODEL, temperature=0)

    chain = llm | StrOutputParser()

    def chat_node(state: MessageState) -> dict:
        response = chain.invoke(state["messages"])
        return {"messages": [AIMessage(content=response)]}

    graph = StateGraph(MessageState)

    graph.add_node("chat_node", chat_node)

    graph.add_edge(START, "chat_node")
    graph.add_edge("chat_node", END)

    app = graph.compile()

    # print("\n--- Mermaid Graph ---")
    # print(app.get_graph().draw_mermaid())

    # png_bytes = app.get_graph().draw_mermaid_png()
    # with open("graph_3.png", "wb") as f:
    #     f.write(png_bytes)

    result = app.invoke({
        "messages": [
            HumanMessage(content="say hello in Telugu")
        ]
    })

    print(result)


def exercise_first_langgraph():
    """
    EXERCISE: Create a LangGraph that:
    1. Takes a topic as input
    2. Node 1: Generates 3 questions about the topic
    3. Node 2: Answers one of the questions
    4. Returns both questions and answer
    """

    class QAState(TypedDict):
        topic: str
        questions: str
        answer: str

    llm = ChatOllama(model=MODEL, temperature=0)

    def generate_questions(state: QAState) -> dict:
        response = llm.invoke(
            f"Generate 3 interesting questions about: {state['topic']}\n"
            "Format: numbered list"
        )
        return {"questions": response.content}

    def answer_question(state: QAState) -> dict:
        response = llm.invoke(
            f"Answer the first question from this list:\n{state['questions']}"
        )
        return {"answer": response.content}

    graph = StateGraph(QAState)
    
    graph.add_node("generate_questions", generate_questions)
    graph.add_node("answer_question", answer_question)

    graph.add_edge(START, "generate_questions")
    graph.add_edge("generate_questions", "answer_question")
    graph.add_edge("answer_question", END)

    app = graph.compile()

    result = app.invoke({"topic": "The future of renewable energy"})

    print("\nExercise Result:")
    print(f"  Topic: {result['topic']}")
    print(f"  Questions: {result['questions']}")
    print(f"  Answer: {result['answer']}")

if __name__ == "__main__":
    exercise_first_langgraph()