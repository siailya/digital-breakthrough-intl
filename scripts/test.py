from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from sklearn.preprocessing import LabelEncoder
import pickle
import pandas as pd


pkl_file = open('executor_label_encoder.pkl', 'rb')
le = pickle.load(pkl_file) 


tokenizer = AutoTokenizer.from_pretrained("ai-forever/sbert_large_mt_nlu_ru")
model = AutoModelForSequenceClassification.from_pretrained("/work/hack/executor_model_on_my_clear_data/checkpoint-test")
model = model.to("cuda")
model.eval()

tokenized_input = tokenizer(["Крик души что происходит с горячей водой"], truncation=True, max_length=512, padding=True, return_tensors='pt')
tokenized_input = tokenized_input.to("cuda")

with torch.no_grad():
    result = model(**tokenized_input)
predict = torch.argmax(result.logits.detach().cpu(), axis=1)

print(le.inverse_transform(predict))
print(result)