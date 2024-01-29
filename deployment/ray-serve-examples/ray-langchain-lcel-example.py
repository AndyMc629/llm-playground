'''
Examples below adapted from https://python.langchain.com/docs/integrations/providers/ray_serve
'''

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
#from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
model = ChatOpenAI(model="gpt-4")
output_parser = StrOutputParser()

chain = prompt | model | output_parser

chain.invoke({"topic": "ice cream"})


# 0: Import ray serve and request from starlette
from ray import serve
from starlette.requests import Request


# 1: Define a Ray Serve deployment.
@serve.deployment
class LLMServe:
    def __init__(self) -> None:
        # All the initialization code goes here
        pass

    async def __call__(self, request: Request) -> str:
        # You can parse the request here
        # and return a response
        return "Hello World" #v1 has no LLM!


# 2: Bind the model to deployment
deployment = LLMServe.bind()

# 3: Run the deployment
serve.api.run(deployment)

import requests
text = "dummy"
PORT_NUMBER = 8000 #you can see this in the second or third line of the spin up logs
response = requests.post(f"http://localhost:{PORT_NUMBER}/?text={text}")
print(response.content.decode())

# Shutdown the deployment
serve.api.shutdown()