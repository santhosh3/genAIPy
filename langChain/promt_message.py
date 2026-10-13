from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import (
    AIMessage,
    ChatMessage,
    HumanMessage,
    ToolMessage,
    SystemMessage
)


# # chat Template
# prompt = ChatPromptTemplate.from_template("Tell me {adjective} joke about the {topic}")

# # message and inspect
# message = prompt.format_messages(adjective="funny",topic="chicken")


# prompt1 = ChatPromptTemplate.from_messages([
#     ("system", "you are helpful assistant that translate {input_language} to {output_language}"),
#     ("human", "Translate the following text:{text}")
# ])

# model = ChatOllama(model="qwen3:1.7b", temperature=0.7)

# parser = StrOutputParser()

# message1 = prompt1.format_messages(
#     input_language="english",
#     output_language="telugu",
#     text="mother")

# result = model.invoke(message1)
# #        model.generate([message1])
# print(result.content)


# messages = [
#     HumanMessage(content="Hello how are you"),
#     AIMessage(content="Hi there, how can I assist today"),
#     SystemMessage(content="This is a system message"),
#     ToolMessage(content="Tool execution successful"),
#     ChatMessage(content="This is general chat message")
# ]

system_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}")
])

user_prompt = ChatPromptTemplate.from_messages([
    ("user", "{question}")
])

prompt = system_prompt + user_prompt

model = ChatOllama(
    model="qwen3:1.7b",
    temperature=0.7
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({
    "role": "helpful assistant",
    "question": "What is AI?"
})

print(result)