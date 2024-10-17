import torch
from sklearn.metrics import f1_score


class Metrics:
    # def __init__(self, outputs):
    #     batch_preds = [x['preds'] for x in outputs]
    #     batch_probs = [x['probs'] for x in outputs]
    #     batch_labels = [x['labels'] for x in outputs]

    #     self.preds = torch.cat(batch_preds)
    #     self.labels = torch.cat(batch_labels)
    #     self.probs = torch.cat(batch_probs)

    @staticmethod
    def accuracy(correct_predictions, dataset):
        return correct_predictions / (2 * len(dataset))

    @staticmethod
    def f1_score(labels, preds):
        return f1_score(labels.cpu(), preds.cpu(), average='macro')
