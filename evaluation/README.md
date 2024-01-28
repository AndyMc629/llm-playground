# LLM Evaluation Resources
This folder contains resources for getting started with evaluating LLMs.

## 1. MLFlow Evaluate API
BROKEN! - 18/1/2024

## 2. RAGAs
```python
from ragas import evaluate
from datasets import Dataset
import os

os.environ["OPENAI_API_KEY"] = "your-openai-key"

# prepare your huggingface dataset in the format
# Dataset({
#     features: ['question', 'contexts', 'answer', 'ground_truths'],
#     num_rows: 25
# })

dataset: Dataset

results = evaluate(dataset)
```


### Resources

1. https://dev.to/guybuildingai/-top-5-open-source-llm-evaluation-frameworks-in-2024-98m
