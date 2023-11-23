import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, DataCollatorWithPadding
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict
import evaluate
import numpy as np
import torch


torch.manual_seed(42)


accuracy = evaluate.load("accuracy")
f1_metric = evaluate.load("f1")

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return {
        "accuracy": accuracy.compute(predictions=predictions, references=labels),
        "f1_weighted": f1_metric.compute(predictions=predictions, references=labels, average="weighted")
        }

def preprocess_logits_for_metrics(logits, labels):
    return logits[0]


def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True, max_length=512, padding=True)


train = pd.read_csv("/work/hack/train_dataset.csv")
test = pd.read_csv("/work/hack/test_dataset.csv")
train = train.rename(columns={"subject": "labels"})
test = test.rename(columns={"subject": "labels"})

le = LabelEncoder()
train['labels'] = le.fit_transform(train['labels'])
test['labels'] = le.transform(test['labels'])


model_name = "ai-forever/sbert_large_nlu_ru"
batch_size = 10

train_dataset = Dataset.from_pandas(train)
test_dataset = Dataset.from_pandas(test)

ds = DatasetDict()

ds['train'] = train_dataset
ds['test'] = test_dataset

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=len(le.classes_)
)
tokenized_ds = ds.map(preprocess_function, batched=True)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

training_args = TrainingArguments(
    output_dir="subject_model_on_my_clear_data",
    learning_rate=3e-5,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    eval_accumulation_steps=1,
    num_train_epochs=10,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    lr_scheduler_type="cosine",  
    load_best_model_at_end=True,
    push_to_hub=False,
    label_names=["labels"],
    report_to="none",
    label_smoothing_factor=0.01,
    fp16=True
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_ds["train"],
    eval_dataset=tokenized_ds["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    #preprocess_logits_for_metrics=preprocess_logits_for_metrics
)

trainer.train()
trainer.evaluate()