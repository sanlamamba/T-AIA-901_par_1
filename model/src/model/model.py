import os
import torch
import torch.nn as nn
from transformers import AutoModel

class BertForSequenceClassification(nn.Module):
    def __init__(self, n_classes, bert_model=AutoModel.from_pretrained("dbmdz/bert-base-french-europeana-cased")):
        super(BertForSequenceClassification, self).__init__()
        self.bert = bert_model
        self.drop = nn.Dropout(p=0.3)
        self.out_linear = nn.Linear(self.bert.config.hidden_size, n_classes)


    def forward(self, input_ids, attention_mask):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        pooled_output = outputs[1]

        output_depart = self.out_linear(self.drop(pooled_output))

        return output_depart

    def save_weights_and_biases(self, file_name:str, path:str=None):
        if path != None:
            model_path= os.path.join(path, f"{file_name}")
        else: 
            model_path= os.path.join(os.getcwd(), f"../../processed/model_2/{file_name}")
        state_dict = {k.replace("module.", ""): v for k, v in self.state_dict().items()}
        torch.save(state_dict, model_path)

    def load(self, file_name, path = None):
        if path:
            model_path = os.path.join(path, f"{file_name}")
        else:
            model_path = os.path.join(os.getcwd(), f"../../processed/model_2/{file_name}")
        self.load_state_dict(torch.load(model_path, weights_only=True))