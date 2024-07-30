from django.shortcuts import render
from django.http import JsonResponse
import json
import os
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_md")

# Load responses
with open(os.path.join(os.path.dirname(__file__), 'responses.json')) as f:
    responses = json.load(f)["responses"]

# Function to find the most similar word
def find_similar_word(word, word_list):
    word_nlp = nlp(word)
    max_sim = -1
    best_match = None
    for candidate in word_list:
        candidate_nlp = nlp(candidate)
        sim = word_nlp.similarity(candidate_nlp)
        if sim > max_sim:
            max_sim = sim
            best_match = candidate
    return best_match

def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question', '')

        # Tokenize the input question
        doc = nlp(question)
        matched_words = []
        for token in doc:
            similar_word = find_similar_word(token.text, responses)
            if similar_word:
                matched_words.append(similar_word)

        # Form the response
        response = ' '.join(matched_words)

        return JsonResponse({'response': response})
    return render(request, 'chatbot_app/index.html')