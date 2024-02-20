Follow along here https://blog.llamaindex.ai/tonic-validate-x-llamaindex-implementing-integration-tests-for-llamaindex-43db50b76ed9 

1. Install Node.js

```
brew install node
```

2. Create exemplar RAG setup


```
npx create-llama@latest
```

3. Answer prompts

```
What is your project named? » llama-validate-demo
Which template would you like to use? » Chat without streaming
Which framework would you like to use? » FastAPI (Python)
Would you like to install dependencies automatically? » No
Which model would you like to use? » gpt-3.5-turbo
Which data source would you like to use? » Use an example PDF
Would you like to use a vector database? » No, just store the data in the file system
```

4. For me, activate conda env

```
conda activate oxford-demo-rag-tonic
```

5. Poetry stuff (root folder of created app):

```
pip install poetry
poetry install
```

6. 
