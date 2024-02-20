'''
Examples below adapted from https://python.langchain.com/docs/integrations/providers/ray_serve
'''

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
#from langchain_openai import ChatOpenAI

#################################
# A. Simple LCEL Example
prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
model = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()

#LCEL syntax
chain = prompt | model | output_parser

#Run the chain
chain.invoke({"topic": "ice cream"})
#################################


#################################
# B. Basic Ray Serve Example
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
#################################


#################################
# C. Deploy LLM with Ray Serve
from ray import serve
from starlette.requests import Request

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI

@serve.deployment
class DeployLLM:
    def __init__(self):
        # We initialize the LLM, template and the chain here
        prompt = ChatPromptTemplate.from_template(
            "Question: {question}\n\nAnswer: Let's think step by step."
            )
        model = ChatOpenAI(model="gpt-3.5-turbo")
        output_parser = StrOutputParser()
        self.chain = prompt | model | output_parser

    def _run_chain(self, question: str):
        """
        Run the chain with the given question.

        :param question: str - the question to be passed to the chain
        :return: the result of invoking the chain with the given question
        """
        return self.chain.invoke({"question": question})

    async def __call__(self, request: Request):
        # 1. Parse the request
        text = request.query_params["text"]
        # 2. Run the chain
        resp = self._run_chain(text)
        # 3. Return the response
        return resp
    
deployment = DeployLLM.bind()
serve.api.run(deployment)


text = "What is the meaning of life?"
PORT_NUMBER = 8000 #you can see this in the second or third line of the spin up logs
response = requests.post(f"http://localhost:{PORT_NUMBER}/?text={text}")
print(response.content.decode())

# Shutdown the deployment
serve.api.shutdown()
#################################