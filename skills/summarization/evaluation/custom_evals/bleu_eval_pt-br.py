import numpy as np
from typing import Dict, TypedDict, Union, Any
import nltk
from nltk.translate.bleu_score import sentence_bleu
from nltk.tokenize import word_tokenize

# Download required NLTK data
nltk.download('punkt', quiet=True)

def nltk_bleu_eval(output, ground_truth) -> float:
    """
    Calculate BLEU score using NLTK and evaluate against a threshold.
    
    Args:
    output (str): The output to evaluate.
    ground_truth (str): The ground_truth output.
    threshold (float): The threshold para the BLEU score (padrão: 0.5).
    
    Retorna:
    tuple: (float, bool) - The BLEU score and whether isso passes the threshold.
    """
    # Tokenize the summaries
    output_tokens = word_tokenize(output.lower())
    ground_truth_tokens = word_tokenize(ground_truth.lower())
    
    try:
        # Calculate BLEU score
        # NOTA: sentence_bleu expects a list of Referências, so we wrap reference_tokens in a list
        bleu_score = sentence_bleu([ground_truth_tokens], output_tokens, weights=(0.25, 0.25, 0.25, 0.25))
        
        # Ensure bleu_score is a float
        if isinstance(bleu_score, (int, float)):
            bleu_score_float = float(bleu_score)
        elif isinstance(bleu_score, (list, np.ndarray)):
            # se isso's a list or lista, take the mean
            bleu_score_float = float(np.mean(bleu_score))
        else:
            # se isso's neither a número nor a list, padrão to 0
            print(f"Warning: Unexpected BLEU score type: {type(bleu_score)}. Defaulting to 0.")
            bleu_score_float = 0.0
    except Exception as e:
        print(f"Error calculating BLEU score: {e}. Defaulting to 0.")
        bleu_score_float = 0.0
    
    # retornar both the BLEU score and whether isso passes the threshold
    return bleu_score_float


def get_assert(output: str, context, threshold=0.3) -> Union[bool, float, Dict[str, Any]]:
    ground_truth = context['vars']['ground_truth']
    score = nltk_bleu_eval(output, ground_truth)
    
    if score >= threshold:
        return {
            "pass": True,
            "score": score,
            "reason": "Average score is above threshold"
        }
    else:
        return {
        "pass": False,
        "score": score,
        "reason": "Average score is below threshold"
        }