#!/usr/bin/env python
# train.py - Train deep learning model to answer questions about Jira tickets.
__version__ = '0.0.1'
__author__ = 'Forest Mars'

import torch
import pandas as pd
from transformers import T5Tokenizer, T5ForConditionalGeneration, Adafactor


EPOCHS = 100
BATCHES = 1
batch_size=8
loss_per_10_steps = []


if torch.cuda.is_available():
    print("CUDA available")
    dev = torch.device("cuda:0")
else:
    print("CUDA not available")
    dev = torch.device("cpu")

train_df = pd.read_csv('jira-nlg-data.csv', index_col=[0])
train_df = train_df.iloc[  :35000,:]
train_df = train_df.sample(frac = 1)
num_of_batches=len(train_df)/batch_size

tokenizer = T5Tokenizer.from_pretrained('t5-base')

model = T5ForConditionalGeneration.from_pretrained('t5-base', return_dict=True)
model.to(dev)
model.train()  # sets mode but doesn't train

optimizer = Adafactor(model.parameters(),
    lr=1e-3,
    eps=(1e-30, 1e-3),
    clip_threshold=1.0,
    decay_rate=-0.8,
    beta1=None,
    weight_decay=0.0,
    relative_step=False,
    scale_parameter=False,
    warmup_init=False)

for epoch in range(1, EPOCHS+1):
  running_loss = 0
  for i in range(BATCHES):
    inputbatch = []
    labelbatch = []
    new_df = train_df[i*batch_size:i*batch_size+batch_size]
    for indx,row in new_df.iterrows():
      input = 'WebNLG: '+row['input_text']+'</s>'
      labels = row['target_text']+'</s>'
      inputbatch.append(input)
      labelbatch.append(labels)
    inputbatch = tokenizer.batch_encode_plus(
        inputbatch,padding=True,
        max_length = 400,
        return_tensors = 'pt') ["input_ids"]
    labelbatch = tokenizer.batch_encode_plus(
        labelbatch,padding=True,
        max_length=400,
        return_tensors="pt") ["input_ids"]
    inputbatch = inputbatch.to(dev)
    labelbatch = labelbatch.to(dev)

    optimizer.zero_grad()

    outputs = model(input_ids=inputbatch, labels=labelbatch)

    loss = outputs.loss
    loss_num = loss.item()
    logits = outputs.logits
    running_loss += loss_num
    if i%10 ==0:
      loss_per_10_steps.append(loss_num)

    loss.backward()

    optimizer.step()

  running_loss=running_loss/int(num_of_batches)

  print('Epoch: {} , Running loss: {}'.format(epoch,running_loss))


torch.save(model.state_dict(),'pytorch_model.bin')
