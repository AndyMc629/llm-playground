# Based loosely on https://www.pinecone.io/learn/series/langchain/langchain-agents/
from langchain.chains import LLMMathChain
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_openai import ChatOpenAI
from langchain import hub

import os

# turn on wandb logging for langchain
os.environ["LANGCHAIN_WANDB_TRACING"] = "true"
# optionally set your wandb settings or configs
os.environ["WANDB_PROJECT"] = "langchain-tracing"
# grab my OPENAI_API_KEY
openai_api_key = os.getenv("OPENAI_API_KEY")
#print(openai_api_key) #for debugging

# instantiate the LLM and MathChain
llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
llm_math = LLMMathChain(llm=llm)

# Give this chain a tool
math_tool = Tool(
    name="Math",
    func=llm_math.run,
    description="Useful for doing maths."
)

tools = [math_tool]
#prompt = hub.pull("hwchase17/openai-tools-agent") #basic react agent
prompt = hub.pull("hwchase17/react")

math_react_agent = create_react_agent(
    llm=llm, 
    tools=tools, 
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=math_react_agent,
    tools=tools,
    verbose=True
)

agent_executor.invoke({"input": "What is the square root of 144?"})

# some sample maths questions
questions = [
  "Find the square root of 5.4.",
  "What is 3 divided by 7.34 raised to the power of pi?",
  "What is the sin of 0.47 radians, divided by the cube root of 27?"
]

for question in questions:
  try:
    # call your Agent as normal
    answer = agent_executor.invoke({"input": question})
    print(answer)
  except Exception as e:
    # any errors will be also logged to Weights & Biases
    print(e)
    pass
