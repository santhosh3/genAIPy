from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, SimpleJsonOutputParser
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from langchain.chat_models import init_chat_model

load_dotenv()

def demo_basic_chain(): 
    """Demonstrate the basic chain using LCEL."""

    # Best Practice: Separate system behavior from user input
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer in one sentence."),
        ("user", "{question}")
    ])

    set_llm_cache(InMemoryCache())

    # Introduce our model here
    model = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.7,
    )

    # Introduce our parser here
    parser = StrOutputParser()

    # Execute our chain
    chain = prompt | model | parser

    # Invoke the chain with the input variable
    result = chain.invoke({"question": "What is LangChain?"})

    print(f"Response: {result}")

    return chain

def demo_batch_execution():
    prompt = ChatPromptTemplate.from_messages([
      ("system", "You are a helpful assistant. Answer in one sentence."),
      ("user", "{question}") # Expects "question"
    ])
    
    # Introduce our model here
    model = ChatOllama(model="qwen3:1.7b", temperature=0.7)
    
    # Introduce our parser here
    parser = StrOutputParser()
    
    # Execute our chain
    chain = prompt | model | parser

    # Raise the inputs for my Prompts (Changed "text" to "question")
    inputs = [
        {"question" : "Hello, How are you?"},
        {"question" : "What is Your name?"},
        {"question" : "What are you good at?"}
    ]

    # Use .batch() instead of .invoke()
    results = chain.batch(inputs)

    # The result is a list of strings
    for i, res in enumerate(results):
        print(f"Question: {inputs[i]['question']}")
        print(f"Response: {res}\n")

def demo_stream_execution():
    prompt = ChatPromptTemplate.from_messages([
      ("system", "Write a haiku about ."),
      ("user", "{question}") # Expects "question"
    ])
    
    # Introduce our model here
    model = ChatOllama(model="qwen3:1.7b", temperature=0.7)
    
    # Introduce our parser here
    parser = StrOutputParser()
    
    # Execute our chain
    chain = prompt | model | parser

    # run with Streaming enabled
    for chunk in chain.stream({"question" : "nature"}):
        print(chunk, end="", flush=True)

def demo_schema_inspect():
    prompt = ChatPromptTemplate.from_messages([
      ("system", "Write a haiku about ."),
      ("user", "{question}") # Expects "question"
    ])
    
    # Introduce our model here
    model = ChatOllama(model="qwen3:1.7b", temperature=0.7)
    
    # Introduce our parser here
    parser = StrOutputParser()
    
    # Execute our chain
    chain = prompt | model | parser

    input_schema = chain.input_schema.model_json_schema()
    output_schema = chain.output_schema.model_json_schema()

    print(f"Input schema: {input_schema}")
    print(f"Output schema: {output_schema}")

def run_flexible_chain(model_name: str, provider: str):
    prompt = ChatPromptTemplate.from_messages([
      ("system", "You are a helpful assistant. Answer in one sentence. Return your answer ONLY as valid JSON"),
      ("user", "{question}")
    ])
    
    # Initialize dynamically based on inputs
    model = init_chat_model(model=model_name, model_provider=provider, temperature=0.7)
    
    parser = SimpleJsonOutputParser()
    chain = prompt | model | parser

    inputs = [
        {"question": "What is LangChain?"},
        {"question": "How does dynamic model routing work? explain clearly with examples"}
    ]

    results = chain.batch(inputs)

    for i, res in enumerate(results):
        print(f"[{model_name}] Question: {inputs[i]['question']}")
        print(f"[{model_name}] Response: {res}\n")

if __name__ == "__main__":
    demo_basic_chain()

