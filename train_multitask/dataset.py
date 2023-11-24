from torch.utils.data import Dataset, DataLoader
import pandas as pd
from typing import List
import datasets
from transformers import DataCollatorWithPadding
from sklearn.preprocessing import LabelEncoder


class MultiTaskDataset(Dataset):
    def __init__(self, tokenizer, path_to_dataset: str, labels: List[str], batch_size: int = 10):
        self.df = pd.read_csv(path_to_dataset)
        self.labels = labels
        self.batch_size = batch_size
        self.tokenizer = tokenizer
        self.label_encoders = []
        self.dataloader = self._create_dataloader(self.df, labels)
        
    
    def _preprocess_function(self, sentences):
        return self.tokenizer(sentences['text'], truncation=True, max_length=512, padding=True)

    
    def _create_dataloader(self, pandas_dataframe, labels: List[str]):
        for i in range(len(labels)):
            le = LabelEncoder()            
            pandas_dataframe[f"labels_{labels[i]}"] = le.fit_transform(pandas_dataframe[labels[i]])
            self.label_encoders.append(le)
            
        dataset = datasets.Dataset.from_pandas(pandas_dataframe)
        for i in range(len(labels)):
            dataset = dataset.remove_columns(labels[i])
            
        dataset = dataset.map(self._preprocess_function, batched=True)
        dataset = dataset.remove_columns("text")
        dataset = dataset.with_format("torch")
        return enumerate(DataLoader(dataset, batch_size=self.batch_size, shuffle=False, num_workers=1))


    def __getitem__(self, index):
        return next(self.dataloader)[1]
    
    
    def update_dataloader(self):
        self.dataloader = self._create_dataloader(self.df, self.labels)
    
    
    def get_classes_cnt_labels(self):
        return [len(le.classes_) for le in self.label_encoders]
    
    
    def __len__(self):
        return len(self.df)