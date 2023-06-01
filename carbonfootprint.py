import json
import numpy as np

def load_json(file):
    with open(file) as bot_responses:
        return json.load(bot_responses)
    
response_data = load_json("data.json")

def get_response(user_input: str) -> str:
    if user_input =="":
        return "Im right here, just let me know when you need me."
    user_input_lower = user_input.lower()
    user_keywords = user_input.lower().split()
    scores = np.zeros(len(response_data))
    for i, response in enumerate(response_data):
        keywords = response['keywords']
        try:
            if np.char.equal(user_keywords,keywords).all():
                scores[i] += len(user_keywords)
                continue
        except ValueError:
            pass
        for keyword in keywords:
            matches = np.isin(keyword, user_keywords)
            if matches.all():
                scores[i] += 1
            if user_input_lower==keyword:
                scores[i] += 1
        scores[i] += np.sum(matches)
    max_score = np.max(scores)
    max_score_indices = np.where(scores == max_score)[0]
    if max_score > 0 and len(max_score_indices) > 0:
        random_index = np.random.choice(max_score_indices)
        return response_data[random_index]["response"]
    else:
        return "I'm sorry, I couldn't find a matching response."

if __name__ == '__main__':
    while True:
        user_input = input("You: ")
        print("Bot:", get_response(user_input))
