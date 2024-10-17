import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from tqdm import tqdm
from utils.data_loader import DeviceDataLoader
from utils.metrics import Metrics


class Trainer:
    def __init__(
        self, 
        model, 
        data_loader_train, 
        data_loader_valid, 
        learning_rate = 2e-5,
        optimizer = None, 
        loss_fn = nn.CrossEntropyLoss(), 
    ):
        self.model = model
        self.data_loader_train = data_loader_train
        self.data_loader_valid = data_loader_valid
        self.loss_fn = loss_fn
        self.optimizer = optimizer
        self.history = []

        if self.optimizer is None:
            self.optimizer = optim.Adam(
                filter(lambda p: p.requires_grad, model.parameters()),
                lr=learning_rate
            )

    def train_epoch(self, current_epoch):
        train_outputs = []
        val_outputs = []
        losses_train = []
        losses_valid = []
        correct_predictions_train = 0
        correct_predictions_valid = 0
        device = DeviceDataLoader.get_default_device()

        self.model.train()
        with tqdm(total=len(self.data_loader_train), desc=f"Epoch {current_epoch}", unit="batch") as pbar:
            for d in self.data_loader_train:
                self.training_step(d, device, correct_predictions_train, losses_train, train_outputs)
                pbar.update(1)

        self.model.eval()
        for d in self.data_loader_valid:
            self.validation_step(
                d,
                device,
                correct_predictions_valid,
                losses_valid,
            )

        train_results = self.epoch_end(
            correct_predictions_train,
            losses_train,
            self.data_loader_train.dataset,
            depart_labels=self.data_loader_train.labels["departure"],
            depart_outputs=train_outputs.depart,
            arrival_labels=self.data_loader_train.labels["arrival"],
            arrival_outputs=train_outputs.arrival
        )
        val_results = self.epoch_end(
            correct_predictions_valid,
            losses_valid,
            self.data_loader_valid.dataset,
            depart_labels=self.data_loader_valid.labels["departure"],
            depart_outputs=val_outputs.depart,
            arrival_labels=self.data_loader_valid.labels["arrival"],
            arrival_outputs=val_outputs.arrival
        )

        return {
            "train_acc": train_results.acc,
            "train_loss": train_results.loss,
            "train_f1": train_results.f1,
            "valid_acc": val_results.acc,
            "valid_loss": val_results.loss,
            "val_f1": val_results.f1
        }

    def run_trainer(self, n_epochs):
        for epoch in range(n_epochs):
            results = self.train_epoch(epoch)
            self.model.epoch_end(epoch, results)
            print(results)
            self.history.append(results)

    def training_step(self, batch, device, correct_predictions_train, losses_train):
        input_ids = DeviceDataLoader.to_device(batch["input_ids"], device)
        attention_mask = DeviceDataLoader.to_device(batch["attention_mask"], device)
        labels_depart = DeviceDataLoader.to_device(batch["departure"], device)
        labels_arrival = DeviceDataLoader.to_device(batch["arrival"], device)

        self.optimizer.zero_grad()

        outputs_depart, outputs_arrival = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        loss_depart = self.loss_fn(outputs_depart, labels_depart)
        loss_arrival = self.loss_fn(outputs_arrival, labels_arrival)
        loss = loss_depart + loss_arrival

        correct_predictions_train += (outputs_depart.argmax(1) == labels_depart).sum().item()
        correct_predictions_train += (outputs_arrival.argmax(1) == labels_arrival).sum().item()

        losses_train.append(loss.item())

        loss.backward()
        self.optimizer.step()

    def validation_step(self, batch, device, correct_predictions_valid, losses_valid):
            input_ids = DeviceDataLoader.to_device(batch["input_ids"], device)
            attention_mask = DeviceDataLoader.to_device(batch["attention_mask"], device)
            labels_depart = DeviceDataLoader.to_device(batch["departure"], device)
            labels_arrival = DeviceDataLoader.to_device(batch["arrival"], device)

            outputs_depart, outputs_arrival = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

            loss_depart = self.loss_fn(outputs_depart, labels_depart)
            loss_arrival = self.loss_fn(outputs_arrival, labels_arrival)
            loss =  loss_depart + loss_arrival

            correct_predictions_valid += (outputs_depart.argmax(1) == labels_depart).sum().item()
            correct_predictions_valid += (outputs_arrival.argmax(1) == labels_arrival).sum().item()

            losses_valid.append(loss.item())

    def epoch_end(self, correct_predictions, losses, dataset, depart_labels, depart_outputs, arrival_labels, arrival_outputs):
        acc = Metrics.accuracy(correct_predictions, dataset)
        loss = np.mean(losses)
        depart_f1 = Metrics.f1_score(depart_labels, depart_outputs)
        arrival_f1 = Metrics.f1_score(arrival_labels, arrival_outputs)

        return {"acc": acc, "loss": loss, "depart_f1": depart_f1, "arrival_f1": arrival_f1}

    # def epoch_end(self, epoch, result):
    #     print(f"Epoch [{epoch}], train_loss: {result['train_loss']:.4f}, val_loss: {result.val_loss:.4f}, val_acc: {result.val_acc:.4f}, f1_score:{result.f1:.4f}")

    @staticmethod
    @torch.no_grad()
    def evaluate(model, val_loader):
        model.eval()
        outputs = [Trainer.validation_step(model, batch) for batch in val_loader]
        return Trainer.validation_epoch_end(model, outputs)
