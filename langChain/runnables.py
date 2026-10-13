from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableBranch,
    RunnableParallel, 
    RunnablePassthrough,
    RunnableLambda
)
from langchain_ollama import ChatOllama

# model = ChatOllama(
#     model="qwen3:1.7b",
#     temperature=0.7,
#     cache=False
# )

# parser = StrOutputParser()

# summary_chain = (
#     ChatPromptTemplate.from_template(
#         "Summarize this in one sentence:\n{text}"
#     )
#     | model
#     | parser
# )

# keyword_chain = (
#     ChatPromptTemplate.from_template(
#         "Give me 3 keywords for this:\n{text}"
#     )
#     | model
#     | parser
# )

# parallel_chain = RunnableParallel(
#     summary=summary_chain,
#     keywords=keyword_chain
# )

# result = parallel_chain.invoke({
#     "text": "LangChain is a framework for developing applications powered by language models."
# })

# print(result)

# def clean_text(text):
#     return text.strip().lower()

# chain = (
#     RunnableLambda(clean_text)
#     | model
#     | parser
# )

# result = chain.invoke("   What is LangChain?   ")


# chain = RunnablePassthrough()

# result = chain.invoke("Hello")

# print(result)

# chain = RunnableParallel(
#     original=RunnablePassthrough(),
#     modified=lambda x: x.upper()
# )

# result = chain.invoke("hello")

# print(result)
#===========================================================================================
# from langchain_core.runnables import (
#     RunnableParallel,
#     RunnablePassthrough,
#     RunnableLambda
# )

# chain = RunnableParallel(
#     original=RunnablePassthrough(),
#     uppercase=RunnableLambda(lambda x: x.upper()),
#     length=RunnableLambda(lambda x: len(x))
# )

# result = chain.invoke("hello")
# print(result)



def demoPassThroughChain():
    prompt = ChatPromptTemplate.from_template(
        "Original question: {question}\n"
        "Context: {context}\n\n"
        "Answer the question based on the context."
    )

    def fake_retriever(input_dict):
        return " LangChain was created by Harrison Chase in 2022."

    chain = (
        RunnableParallel(
            context=RunnableLambda(fake_retriever), question=RunnablePassthrough()
        )
        | RunnableLambda(
            lambda x: {"context": x["context"], "question": x["question"]["question"]}
        )
        | prompt
        | ChatOllama(model="qwen3:1.7b")
        | StrOutputParser()
    )

    result = chain.invoke({"question": "Who created LangChain?"})
    return f"Answer: {result}"


def demo_chain_branching():
    """A chain that demonstrates branching functionality."""
    model = ChatOllama(model="qwen3:1.7b")

    # Different prompts for different intents
    code_prompt = ChatPromptTemplate.from_template(
        "You are a coding expert. Help with: {input}"
    )
    general_prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant. Answer: {input}"
    )

    # Classifier
    classifier_prompt = ChatPromptTemplate.from_template(
        "Classify this as 'code' or 'general': {input}\nReturn only the classification."
    )
    classifer = classifier_prompt | model | StrOutputParser()

    # Branching chain  based on classification
    def is_code_question(input_dict):
        classification = classifer.invoke(input_dict)
        return "code" in classification.lower()

    branch = RunnableBranch(
        (is_code_question, code_prompt | model | StrOutputParser()),
        general_prompt | model | StrOutputParser(),  # default branch
    )

    # Test
    questions = [
        "How do I write a for loop in Python?",
        "What's the weather like today?",
    ]
    for q in questions:
        result = branch.invoke({"input": q})
        print(f"Q: {q}")
        print(f"A: {result}...\n")



def demoDebugging():
    prompt = ChatPromptTemplate.from_template("Say hello to name: {name}")
    model = ChatOllama(model="qwen3:1.7b")
    chain = prompt | model | StrOutputParser()
    print("Chain input schema", chain.input_schema.model_json_schema)
    print("Chain output schema", chain.output_schema.model_json_schema)
    result = chain.with_config(run_name="greeting name").invoke({"name" : "chinna"})
    print(result)

demoDebugging()