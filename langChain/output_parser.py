from langchain_core.output_parsers import (
    StrOutputParser,
    JsonOutputParser,
    PydanticOutputParser
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

prompt = ChatPromptTemplate.from_template(
    "Return a JSON object with name and age for: {description}"
)

llm = ChatOllama(model="qwen3:1.7b")

parser = JsonOutputParser()

chain = prompt | llm | parser

result = chain.invoke({"description" : "A 20 years old developer name chinna"})

print(type(result))

# Pydantic obj validation output parser

# class Person(BaseModel):
#     name : str = Field(description="The person's name")
#     age : int = Field(description="The person's age")
#     occupation : str = Field(description="The person's occupation")

# parser1 = PydanticOutputParser(pydantic_object=Person)

# prompt1 = ChatPromptTemplate.from_template(
#     "Return 'name', 'age', and 'occupation' of the person for: {description}"
# ).partial(format_instructions=parser1.get_format_instructions())

# llm = ChatOllama(model="qwen3:1.7b")

# chain = prompt1 | llm | parser1

# result = chain.invoke({"description": "A 30-year-old artist named Maria"})

# print(result)

# Structured output using pydentic

class MovieReview(BaseModel):
    title : str = Field(description="The title of the movie")
    review : str = Field(description="A brief review of the movie")
    rating : int = Field(description="The rating of the movie out of 10")

llm = ChatOllama(model="qwen3:1.7b")

structured_model = llm.with_structured_output(MovieReview)

result = structured_model.invoke("Review : Inception is a mind-bended triller. got 9/10 rating")

print(result)