import random
import json
import torch
from model.model import NeuralNet
from lib.nltk_utils import tokenize, bag_of_words


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('lib/intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)


FILE = 'model/data.pth'
data = torch.load(FILE)


input_size = data["input_size"]
output_size = data["output_size"]
hidden_size = data["hidden_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]




model = NeuralNet(input_size, hidden_size, output_size).to(device)

model.load_state_dict(model_state)
model.eval()

bot_name = "Leza"

def get_response(msg):
    sentence = tokenize(msg)

    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)

    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag ==  intent["tag"]:
               return random.choice(intent["responses"])

    return "I do not understand"


