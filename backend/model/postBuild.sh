#!/bin/bash
source conda activate myenv
python -m spacy download fr_core_news_sm
# conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia