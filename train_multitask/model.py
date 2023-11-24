import torch
from typing import List
from transformers import BertModel


class BertHead(torch.nn.Module):
    def __init__(self, cnt_labels: int, hidden_size: int, p: float = 0.1):
        super().__init__()
        self.dropout = torch.nn.Dropout(p)
        self.classifier = torch.nn.Linear(hidden_size, cnt_labels)
    
    def forward(self, x):
        x = self.dropout(x)
        logits = self.classifier(x)
        
        return logits


class MultiTaskBert(torch.nn.Module):
    def __init__(self, backbone_hf: str, labels: List[int], cnt_labels: List[int]):
        super().__init__()
        self.heads = torch.nn.ModuleDict()
        self.labels = labels
        self.backbone = BertModel.from_pretrained(backbone_hf)
        for i in range(len(labels)):
            self.heads[labels[i]] = BertHead(
                cnt_labels=cnt_labels[i], 
                hidden_size=self.backbone.config.hidden_size
            )
    
    def forward(self, x):
        outputs = self.backbone(input_ids=x['input_ids'].squeeze(0), attention_mask=x['attention_mask'].squeeze(0))[1]
        predicts = {label: self.heads[label](outputs) for label in self.labels}
        return predicts