from django.apps import AppConfig
from transformers import ElectraForSequenceClassification, ElectraTokenizer
import torch

class ApiConfig(AppConfig):
    name = 'api'
    tokenizer = ElectraTokenizer.from_pretrained('api/chatbot/koelectra')
    model = ElectraForSequenceClassification.from_pretrained('api/chatbot/checkpoint', num_labels=1)
    torch.cuda.empty_cache()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
