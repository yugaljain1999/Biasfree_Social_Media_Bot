import transformers
import torch
import pandas as pd
import re
#import praw
from modeling_gpt2 import GPT2LMHeadModel
import os

base_dir = '/content/drive/My Drive/GeDiModel/GeDi/'
base_dir2 = '/content/'
if torch.cuda.is_available():
    device = torch.device('cuda')
else:
  device = torch.device('cpu')
def GeDi(MODEL,PRETRAINED_GEDI):
  model = torch.load(os.path.join(base_dir2,MODEL),map_location=device).to(device)  # generate_GeDi.py saves this model(options - topic,detoxify and sentiment)
  gedi_model = torch.load(os.path.join(base_dir,PRETRAINED_GEDI),map_location=device).to(device)
  return model,gedi_model


