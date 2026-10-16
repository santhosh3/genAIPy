
import operator
from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph


MODEL = "qwen3:8b"

model = ChatOllama(model=MODEL, temperature=0)


class ConversationState(TypedDict):
    messages: Annotated[list, operator.add]
    sentiment: str
    count: int


def create_conversation_graph():

    # Node 1: Analyze sentiment
    def analyze_sentiment(state: ConversationState) -> dict:
        last_message = state["messages"][-1]

        chain = model | StrOutputParser()

        response = chain.invoke([
            SystemMessage(
                content=(
                    "Classify sentiment as positive, negative, "
                    "or neutral. Reply with just the word."
                )
            ),
            HumanMessage(content=last_message.content)
        ])

        # Normalize the model output
        sentiment = response.strip().lower()

        if sentiment not in {"positive", "negative", "neutral"}:
            sentiment = "neutral"

        return {"sentiment": sentiment}

    # Node 2: Generate a response based on sentiment
    def generate_response(state: ConversationState) -> dict:
        sentiment = state["sentiment"]
        last_message = state["messages"][-1]

        system_prompts = {
            "positive": (
                "Respond enthusiastically and build on "
                "the user's positive energy."
            ),
            "negative": (
                "Respond empathetically and offer support."
            ),
            "neutral": (
                "Respond helpfully and informatively."
            ),
        }

        prompt = system_prompts.get(
            sentiment, system_prompts["neutral"]
        )

        response = model.invoke([
            SystemMessage(content=prompt),
            HumanMessage(content=last_message.content)
        ])

        return {
            "messages": [
                AIMessage(content=response.content)
            ],
            "count": state.get("count", 0) + 1
        }

    # Create graph
    graph = StateGraph(ConversationState)

    graph.add_node("analyze_sentiment", analyze_sentiment)
    graph.add_node("generate_response", generate_response)

    graph.add_edge(START, "analyze_sentiment")
    graph.add_edge("analyze_sentiment", "generate_response")
    graph.add_edge("generate_response", END)

    return graph.compile()


def demo_conversation():
    app = create_conversation_graph()

    test_messages = [
        "I just got promoted at work! I'm so excited!",
        "My computer crashed and I lost all my work...",
        "What's the weather like today?",
    ]

    for msg in test_messages:
        result = app.invoke({
            "messages": [HumanMessage(content=msg)],
            "sentiment": "",
            "count": 0,
        })

        print(f"Input: {msg}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Response: {result['messages'][-1].content}")
        print(f"Response count: {result['count']}")
        print("-" * 40)


if __name__ == "__main__":
    demo_conversation()
