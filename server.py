
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import json

# load the bert model and tokenizer 
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

# load responses
with open('responses.json') as f:
    responses = json.load(f)["responses"]

# function to classify user question
def classify_question(question):
    inputs = tokenizer(question, return_tensors='pt')
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_id = torch.argmax(logits).item()
    return predicted_class_id

# function to return responses
def get_response(predicted_class_id):
    return responses[predicted_class_id]