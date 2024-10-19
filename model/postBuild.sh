#!/bin/bash
source conda activate myenv
python -m spacy download fr
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia