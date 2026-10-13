from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from typing import List


class QAResponse(BaseModel):
    answer: str = Field(description="The answer to the user's question.")
    confidence: str = Field(description="Confidence level: high, medium, or low")
    reasoning: str = Field(description="The reasoning behind the answer provided.")
    follow_up_questions: List[str] = Field(
        description="A list of follow-up questions related to the topic.",
        default_factory=list,
    )
    sources_needed: bool = Field(
        description="Indicates whether sources are needed for the answer.",
        default=False,
    )


class SmartQABot:
    def __init__(
        self,
        model_name: str = "qwen3:1.7b",
        temperature: float = 0.3,
    ):
        self.model = ChatOllama(
            model=model_name,
            temperature=temperature,
        ).with_structured_output(QAResponse)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a knowledgeable Q&A assistant.

                    Your guidelines:
                    - Answer questions accurately and concisely
                    - Be honest about uncertainty - set confidence to 'low' if unsure
                    - Provide clear reasoning for your answers
                    - Suggest relevant follow-up questions
                    - Indicate if external sources would help

                    Always respond with accurate, helpful information.""",
                ),
                ("human", "{question}"),
            ]
        )
        self.chain = self.prompt | self.model


    def ask(self, question: str) -> QAResponse:
        try:
            response = self.chain.invoke({"question": question})
            return response
        except Exception as e:
            return QAResponse(
                answer="I'm sorry, I couldn't process your question at this time.",
                confidence="low",
                reasoning=str(e),
                follow_up_questions=["Could you please try again later?"],
                sources_needed=True,
            )

    def ask_batch(self, questions: List[str]) -> List[QAResponse]:
        inputs = [{"question": q} for q in questions]
        return self.chain.batch(inputs)


def demo_qa_bot():
    bot = SmartQABot()

    questions = [
        "How do you know all things are you browsing or have you trained with this data. how do you know capital of india"
        "What is the capital of France?",
        "Explain the theory of relativity.",
        "How does photosynthesis work?",
    ]

    print("=" * 60)
    print("SMART Q&A BOT DEMO")
    print("=" * 60)

    for question in questions:
        print(f"\n Question: {question}")
        print("-" * 40)
        response = bot.ask(question)
        print(f"Question: {question}")
        print(f"Answer: {response.answer}")
        print(f"Confidence: {response.confidence}")
        print(f"Reasoning: {response.reasoning}")
        print(f"Follow-up Questions: {response.follow_up_questions}")
        print(f"Sources Needed: {response.sources_needed}")
        print("-" * 60)


def demo_error_handling():
    bot = SmartQABot()

    print("\n" + "=" * 60)
    print("ERROR HANDLING DEMO")
    print("=" * 60)

    # Test with a very long question (edge case)
    long_question = "What is " + "very " * 100 + "important?"

    response = bot.ask(long_question)
    print(f"Handled gracefully: {response.confidence}")


def demo_batch_processing():
    """Demonstrate batch processing."""

    bot = SmartQABot()

    questions = [
        "What is Python?",
        "What is JavaScript?",
        "What is Rust?",
    ]

    print("\n" + "=" * 60)
    print("BATCH PROCESSING DEMO")
    print("=" * 60)

    responses = bot.ask_batch(questions)

    for q, r in zip(questions, responses):
        print(f"\n{q}")
        print(f"  -> {r.answer[:100]}...")
        print(r)



if __name__ == "__main__":

    try:
        #demo_qa_bot()
        demo_batch_processing()
        #demo_error_handling()

        # print("\n" + "=" * 60)
        # print("Section 1 Complete!")
        # print("=" * 60)
        # print(
        # """
        # What you learned:
        # - LangChain ecosystem overview
        # - Environment setup with uv
        # - Core concepts: Runnables, LCEL, pipe operator
        # - Working with multiple LLM providers
        # - Prompt templates and message types
        # - Output parsers and structured output
        # - Building a production Q&A bot
        # """
        # )
    finally:
        pass