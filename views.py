from django.shortcuts import render
from django.http import JsonResponse
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import json
import os

# BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

# Load responses
with open(os.path.join(os.path.dirname(__file__), 'responses.json')) as f:
    responses = json.load(f)["responses"]

# Function to classify user question
def classify_question(question):
    inputs = tokenizer(question, return_tensors='pt')
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_id = torch.argmax(logits).item()
    return predicted_class_id

# Function to generate response sentence from classified index
def generate_response(predicted_class_id):
    response_keywords = [
        ["yok"],
        ["vizyonda", "film"],
        ["şu anda", "vizyonda", "film"],
        ["şimdi", "vizyonda", "film"],
        ["henüz", "vizyonda", "film", "yok"],
        ["film", "bilgi"],
        ["film", "süre"],
        ["film", "rapor"],
        ["!"]
    ]
    return ' '.join(response_keywords[predicted_class_id])

def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question', '')
        predicted_class_id = classify_question(question)
        response = generate_response(predicted_class_id)
        return JsonResponse({'response': response})
    return render(request, 'chatbot_app/index.html')
