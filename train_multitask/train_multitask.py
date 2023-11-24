from dataset import MultiTaskDataset
from transformers import AutoTokenizer
from model import MultiTaskBert
import torch.optim as optim
import torch.nn as nn
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm



tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/distilrubert-small-cased-conversational")
labels = ['executor', 'subject', 'group_subject']
batch_size = 25
train_dataset = MultiTaskDataset(tokenizer, path_to_dataset="/work/hack/train_dataset.csv", labels=labels,batch_size=batch_size)
test_dataset = MultiTaskDataset(tokenizer, path_to_dataset="/work/hack/test_dataset.csv", labels=['executor', 'subject', 'group_subject'])


model = MultiTaskBert(
    backbone_hf="DeepPavlov/distilrubert-small-cased-conversational",
    labels=labels,
    cnt_labels=train_dataset.get_classes_cnt_labels()
)
model = model.to("cuda")
#model = model.half()

cnt_epoch = 5
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=3e-4)


for epoch in range(cnt_epoch):
    train_dataset.update_dataloader()
    test_dataset.update_dataloader()
    train_dataloader = DataLoader(train_dataset, batch_size=1, shuffle=False)
    test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=False)
    model.train()
    running_loss = 0.0
    for step, batch in tqdm(enumerate(train_dataloader)):
        batch = {k: v.to("cuda") for k, v in batch.items()}
        optimizer.zero_grad()
        predicts = model(batch)

        total_loss = 0
        for label in predicts.keys():
            total_loss += criterion(predicts[label], batch[f"labels_{label}"].squeeze(0))
        total_loss = total_loss / len(labels)
        total_loss.backward()
        optimizer.step()
        
        running_loss += total_loss.item()
        
        if step % 500 == 499:
            print(running_loss / 499)
            running_loss = 0
            
            
    model.eval()
    running_loss = 0.0
    acccuracy = {label: 0 for label in labels}
    for step, batch in tqdm(enumerate(test_dataloader)):
        batch = {key: value.to("cuda") for key, value in batch.items()}

        with torch.no_grad():
            predicts = model(batch)
        total_loss = 0
        for label in predicts.keys():
            total_loss += criterion(predicts[label], batch[f"labels_{label}"].squeeze(0))
            acccuracy[label] += (torch.argmax(predicts[label], axis=1) == batch[f"labels_{label}"].squeeze(0)).sum()
        total_loss = total_loss / len(labels)
        running_loss += total_loss.item()
    print(running_loss / len(test_dataset))
    acccuracy = {k: v / len(test_dataset) for k, v in acccuracy.items()} 
    print(acccuracy)
        
    