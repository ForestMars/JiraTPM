
# predict.py - Provides context for answering natural language questions about Jira ticket data.
__version__ = '0.0.1'
__author__ = 'Forest Mars'

import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, Adafactor, BertModel


model = T5ForConditionalGeneration.from_pretrained('t5-base', return_dict=True)
model.load_state_dict(torch.load('pytoch_model.bin'))

for param_tensor in model.state_dict():
    print(param_tensor, "\t", model.state_dict()[param_tensor].size())


"""
checkpoint = torch.load(﻿'load/from/path/model.pth'﻿)
model.load_state_dict(checkpoint[﻿'model_state_dict'﻿]﻿)
optimizer.load_state_dict(checkpoint[﻿'optimizer_state_dict'﻿]﻿)
epoch = checkpoint[﻿'epoch'﻿]
loss = checkpoint[﻿'loss'﻿]
"""

tokenizer = T5Tokenizer.from_pretrained('t5-base')

# model = BertModel.from_pretrained("bert-base-uncased")
# model = T5ForConditionalGeneration.from_pretrained('', return_dict=True)
# model = MyModelDefinition(args)
# model.load_state_dict(torch.load('pytoch_model.bin'))


def _generate(text, model, tokenizer):
    model.eval()  # and there it is. Also, @FIXME (bare function invoking object method)
    input_ids = tokenizer.encode("WebNLG:{} </s>".format(text), return_tensors="pt")
    outputs = model.generate(input_ids) # Why is this behaviour not in a class

    return tokenizer.decode(outputs[0])


def generate(term, model, tokenizer):

    return _generate(term, model, tokenizer)


while True:
    term = input("Enter ticket number:\n")  # eg. Airport
    attrs = input('Enter ticket attributes (eg. assignee, severity) separated by '|': \n')  # eg. Denmark
    ask = term + ' | ' + attrs
    print(ask)
    print(generate(ask, model, tokenizer))
