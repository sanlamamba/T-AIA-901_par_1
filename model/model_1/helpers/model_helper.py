import os

import torch
import torch.nn as nn


class BertForSequenceClassificationBase(nn.Module):
    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except AttributeError:
            return getattr(self.module, name)
 
    def save_weights_and_biases(self, file_name:str, path:str=None):
        if path != None:
            model_path= os.path.join(path, f"{file_name}.pth")
        else: 
            model_path= os.path.join(os.getcwd(), f"../../processed/{file_name}.pth")
        state_dict = {k.replace("module.", ""): v for k, v in self.state_dict().items()}
        torch.save(state_dict, model_path)

    def load(self, file_name, path = None):
        if path:
            model_path = os.path.join(path, f"{file_name}.pth")
        else:
            model_path = os.path.join(os.getcwd(), f"../../processed/{file_name}")
        self.load_state_dict(torch.load(model_path))
