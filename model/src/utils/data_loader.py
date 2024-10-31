import torch
from torch.utils.data import Dataset


class DataEncoderNER(Dataset):
    def __init__(self, sub_sentences, status, tokenizer, max_len):
        self.sub_sentences = sub_sentences
        self.status = status
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.sub_sentences)

    def __getitem__(self, idx):
        encoding = self.tokenizer.encode_plus(
            self.sub_sentences[idx],
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'sub_sentence': self.sub_sentences[idx],
            'status': torch.tensor(self.status[idx], dtype=torch.long)
        }


class DataEncoder(Dataset):
    def __init__(self, sentences, class_name, tokenizer, max_len):
        self.sentences = sentences
        self.class_name = class_name
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, idx):
        encoding = self.tokenizer.encode_plus(
            self.sentences[idx],
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'class_name': torch.tensor(self.class_name[idx], dtype=torch.long),
        }
