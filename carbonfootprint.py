import pandas as pd
import numpy as np
import re


def _load_json(file):
    """
    Load JSON data from a file.

    Args:
        file (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data as a dictionary.
    """
    with open(file) as bot_responses:
        return pd.read_json(file,orient='records')
def _no_match_found():
    no_match_responses = [
    "I'm sorry, I couldn't find a matching response. If you have any questions about reducing your carbon footprint, feel free to ask!",
    "Hmm, it seems I don't have a response for that. However, I'm knowledgeable about carbon footprints. Do you have any questions about reducing yours?",
    "I apologize, but I'm not able to provide a specific answer. On the bright side, I'm well-versed in carbon footprint-related topics. Is there something you'd like to know about it?",
    "Unfortunately, I don't have a response to that. Let's shift the focus to carbon footprints. How can I assist you with reducing yours?",
    "It appears that I don't have the information you're looking for. Let's pivot to the topic of carbon footprints. How can I help you with reducing your impact?",
    "I'm afraid I don't have a response for that, but I'd be happy to discuss ways to lower your carbon footprint. What specific questions do you have?",
    "I'm sorry, I couldn't find a direct answer. However, I can provide insights on minimizing carbon footprint. What would you like to know about it?",
    "Hmm, it seems I can't address your query directly. Nevertheless, I'm well-equipped to discuss ways to reduce your carbon footprint. What would you like to explore?",
    "I'm sorry, I don't have a response for that particular question. Let's talk about carbon footprint instead. How can I assist you in making a positive environmental impact?",
    "Unfortunately, I don't have the information you're seeking. But I'm here to guide you in understanding and minimizing your carbon footprint. What aspects are you curious about?",]
    return np.random.choice(no_match_responses)

def _is_connector(user_input):
    connecting_words = [
        "how", "why", "you", "are", "is", "and", "what", "where", "when", "who",
        "which", "whom", "whose", "will", "would", "could", "can", "should", "do",
        "did", "does", "have", "has", "had", "if", "for","or"
    ]
    return np.any(np.char.equal(user_input, connecting_words))
    
def _clean(string: str)->str:
    return re.sub(r'[^a-z]', '', string.lower())

RESPONSE_DATA = _load_json("data.json")

def get_score(keywords: list, user_input: str) -> float:
    """
    Calculate the score for a list of keywords based on the user input.

    The scoring system works as follows:
    - An exact match between the user input and all keywords in a response contributes a score of 0.6 times the number
      of keywords.
    - For each keyword in the list, the function checks if it exists as a substring in the user input using the
      np.char.find() function. If a keyword is found, a score is assigned based on whether it is a connector word or
      not.
    - Connector words receive a score of 0.3, while other keywords receive a score of 0.5.

    Args:
        keywords (list): A list of keywords to be matched against the user input.
        user_input (str): The user input to be evaluated.

    Returns:
        float: The score calculated based on the matching criteria and scoring system.
    """
    score = 0
    NOT_FOUND = -1
    ALL_KEYWORDS_MATCHED_SCORE = 0.6 * len(keywords)
    CONNECTOR_WORD_SCORE = 0.3
    WORD_SCORE = 0.5
    
    if np.char.equal(user_input, keywords).all():
        score += ALL_KEYWORDS_MATCHED_SCORE
        return score

    for keyword in keywords:
        keyword=_clean(keyword)
        if np.char.find(user_input, keyword) == NOT_FOUND:
            continue

        if _is_connector(keyword):
            score += CONNECTOR_WORD_SCORE
        else:
            score += WORD_SCORE
    return score

def get_response(string_input: str) -> str:
    TOLERANCE = 0.2
    user_input = _clean(string_input)
    if user_input =="":
        return "Im right here, just let me know when you need me." 

    RESPONSE_DATA['score'] = RESPONSE_DATA['keywords'].apply(get_score, user_input=user_input)
    max_score = RESPONSE_DATA['score'].max()
    if not max_score:
        return _no_match_found()
    best_responses = RESPONSE_DATA[RESPONSE_DATA['score'] >= (max_score - TOLERANCE)]
    return best_responses.sample()['response'].values[0]

if __name__ == '__main__':
    while True:
        user_input = input("You: ")
        print("Bot:", get_response(user_input))
