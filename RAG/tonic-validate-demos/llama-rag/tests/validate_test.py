import json
import os
from tonic_validate import ValidateApi
from tonic_validate.metrics import AnswerSimilarityMetric, RetrievalPrecisionMetric, AugmentationPrecisionMetric, AnswerConsistencyMetric
from llama_index.evaluation import TonicValidateEvaluator
import requests

from dotenv import load_dotenv

load_dotenv()

def get_llm_response(prompt):
    url = "http://localhost:8000/api/chat"

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
    headers = { 'Content-Type': 'application/json' }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    result = response['result']
    return result['content'], result['context']

def get_q_and_a():
    # Load qa_pairs.json
    qa_pairs = json.load(open('./tests/qa_pairs.json'))
    return ([x['question'] for x in qa_pairs], [x['answer'] for x in qa_pairs])

def get_responses(questions):
    llm_answers = []
    context_lists = []
    for item in questions:
        llm_answer, llm_context_list = get_llm_response(item)
        llm_answers.append(llm_answer)
        context_lists.append(llm_context_list)
    return (llm_answers, context_lists)

def score_run(questions, context_lists, reference_answers, llm_answers):
    metrics = [
        AnswerSimilarityMetric(),
        RetrievalPrecisionMetric(),
        AugmentationPrecisionMetric(),
        AnswerConsistencyMetric()
    ]
    scorer = TonicValidateEvaluator(metrics, model_evaluator="gpt-4-1106-preview")
    run = scorer.evaluate_run(
        questions, llm_answers, context_lists, reference_answers
    )
    return run, metrics

def test_llama_index():
    questions, reference_answers = get_q_and_a()
    llm_answers, context_lists = get_responses(questions)
    run, metrics = score_run(questions, context_lists, reference_answers, llm_answers)
    # Upload results to web ui
    validate_api = ValidateApi()
    # Get project id from env
    project_id = os.getenv("PROJECT_ID")
    validate_api.upload_run(project_id, run)

    # Check none of the metrics scored too low    
    for metric in metrics:
        if metric.name == AnswerSimilarityMetric.name:
            assert run.overall_scores[metric.name] >= 3.5
        else:
            assert run.overall_scores[metric.name] >= 0.7