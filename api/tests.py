import torch
from transformers import ElectraForSequenceClassification, ElectraTokenizer
from api.chatbot.inference import koelectra_chatbot

def test(user):
    checkpoint = "chatbot/checkpoint"
    path = "chatbot/koelectra"
    tokenizer = ElectraTokenizer.from_pretrained(path)
    model = ElectraForSequenceClassification.from_pretrained(checkpoint, num_labels=1)
    device = torch.device("cuda:7" if torch.cuda.is_available() else "cpu")
    answer = koelectra_chatbot(user['uid'], user['question'], model, tokenizer, device, word_filter=True)
    print(answer)

user = {'uid': 'test', 'question': '공군호텔이 뭐야'}
test(user)
