import pickle

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class InferenceModel:
    def __init__(self, model_path):
        self.model = None
        self.tokenizer = None
        self.le = None

        self.load_checkpoint(f"{model_path}/label_encoder.pkl", f"{model_path}/checkpoint")

    def load_checkpoint(self, label_encoder_path, checkpoint_path):
        pkl_file = open(label_encoder_path, 'rb')
        self.le = pickle.load(pkl_file)
        self.tokenizer = AutoTokenizer.from_pretrained("ai-forever/sbert_large_mt_nlu_ru")
        print(f"Load model at {checkpoint_path}")
        self.model = AutoModelForSequenceClassification.from_pretrained(checkpoint_path)
        self.model = self.model
        self.model.eval()

        print(f"Model at {checkpoint_path} loaded")
        return self.model, self.tokenizer, self.le

    def predict(self, texts):
        tokenized_input = self.tokenizer(texts, truncation=True, max_length=512,
                                         padding=True, return_tensors='pt')
        tokenized_input = tokenized_input

        with torch.no_grad():
            result = self.model(**tokenized_input)
        predict = torch.argmax(result.logits.detach().cpu(), axis=1)

        return self.le.inverse_transform(predict)


if __name__ == '__main__':
    executor_m = InferenceModel("models/executor")
    print(executor_m.predict(["Крик души что происходит с горячей водой",
                              "Добрый день. Территорию чистят от льда?",
                              "Здравствуйте, пришло уведомление от госуслуг, лк как понять в личном кабинете нет информации"]))
