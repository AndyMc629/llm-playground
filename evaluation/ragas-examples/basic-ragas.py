'''
Added a simple example based on https://docs.ragas.io/en/stable/getstarted/evaluation.html#get-started-evaluation


'''

from datasets import load_dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
)


def get_fiqa_eval():
    return load_dataset("explodinggradients/fiqa", "ragas_eval")
    
fiqa_eval = get_fiqa_eval()

# Evaluate on the first 3 examples
results = evaluate(
    fiqa_eval["baseline"].select(range(2)), # selecting only 3
    metrics=[
        context_precision
    ],
)
