import json
import logging
import random
import csv

from flask import request

from routes import app

logger = logging.getLogger(__name__)

with open('words.csv', 'r') as file:
    reader = csv.reader(file)
    word_list = [row[0] for row in reader]
# word_list = ["slate", "lucky", "maser", "gapes", "wages"]

def filter_words(guess, feedback, words):
    for i, (g, f) in enumerate(zip(guess, feedback)):
        if f == 'O':
            words = [word for word in words if word[i] == g]
        elif f == 'X':
            words = [word for word in words if g in word and word[i] != g]
        elif f == '-':
            words = [word for word in words if g not in word]
    return words

def get_next_guess(guess_history, evaluation_history):
    if not guess_history:
        return "slate"  # Starting guess

    last_guess = guess_history[-1]
    last_feedback = evaluation_history[-1]
    possible_words = filter_words(last_guess, last_feedback, word_list)

    if possible_words:
        return random.choice(possible_words)
    else:
        return random.choice(word_list)
    
@app.route('/wordle-game', methods=['POST'])
def wordle_game():

    data = request.get_json()
    guess_history = data.get("guessHistory", [])
    evaluation_history = data.get("evaluationHistory", [])
    next_guess = get_next_guess(guess_history, evaluation_history)
    return json.dumps({"guess": next_guess})

    # logging.info("data sent for evaluation {}".format(data))
    # input_value = data.get("input")
    # result = input_value * input_value
    # logging.info("My result :{}".format(result))
    # return json.dumps(result)
