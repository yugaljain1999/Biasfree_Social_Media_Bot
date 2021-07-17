import discord

import asyncio
import random 
import string

from transformers import GPT2Tokenizer
import torch
import numpy as np
import re
from generate_reply import generate_reply

from main import *
if torch.cuda.is_available():
  device = torch.device('cuda')
else:
  device = torch.device('cpu')
subreddit = 'Depression'
MODEL = 'AG_news_gedi_model_detoxify.pth'
PRETRAINED_GEDI = 'gedi_model_topic.pth'

model,gedi_model = GeDi(MODEL,PRETRAINED_GEDI)
tokenizer = GPT2Tokenizer.from_pretrained('gpt2',do_lower_case=False)


YOURNAME = 'biasfree'
client = discord.Client()

@client.event
async def on_ready():
  print('Logged in {}'.format(client))
  activity = discord.Activity(name = 'Reply to biased comments' , type = discord.ActivityType.watching)
  await client.change_presence(status = discord.Status.online, activity=activity)

def generate(mess,secondary_code):
  print('message',mess)
  multi_code = tokenizer.encode(secondary_code)
  encoded_prompts = tokenizer.encode(mess) # message.content -> input_message
  text = model.generate(input_ids = torch.LongTensor(encoded_prompts).unsqueeze(0).to(device),
                                          pad_lens=None,
                                          max_length= 100,
                                          temperature=0.7,
                                          top_k=40,
                                          top_p=0.9,
                                          repetition_penalty=1.2,
                                          rep_penalty_scale=10,
                                          eos_token_ids = 50256,
                                          pad_token_id = 0,
                                          do_sample=True,
                                          penalize_cond=True,
                                          gedi_model=gedi_model,
                                          tokenizer=tokenizer,
                                          disc_weight=30,
                                          filter_p = 0.8,
                                          target_p = 0.8,
                                          class_bias = 0.0,
                                          attr_class = 1,
                                          multi_code=multi_code) # because mode is "sentiment" here if mode is "topic" then it changes 
                                                          # and we encode secondary code their because then secondary topic will be asked from the user
  text = tokenizer.decode(text.tolist()[0],clean_up_tokenization_spaces = True)
  text = text[len(mess):]
  text = text.replace("||","")
  text = re.sub("||","",text)
  text =  re.sub("||","",text)
  text = re.sub('<|endoftext|>','',text)
  text = text.replace('<|endoftext|>','')
  print('Prompt',mess)

  if text!='||' or text!='.||' or text!=',||' or text!='?||' or text!='':
    if len(text)>=1:
      if text!='||' or text!='':
        t= text
        ch = ['.||','?||',',||','||']
        for c in ch:
          t = t.replace(c,"")
        if re.search('[a-zA-Z]',t):
          print('REPLY',t)
          
  else:
    print('No response')
  return t 
  

@client.event
async def on_message(message):
    if client.user.mention in message.content.replace('<@!', '<@'):
        if message.author == client.user:
            print('.....')
            return
        else:
            if client.is_ready:
                uses_con = False
                async with message.channel.typing():
                  print("Generating")
                  final = ''
                  prefix = ""
                  last_author = ""
                  old = await message.channel.history(limit=1).flatten()
                  old.reverse()
                  for msg in old:
                      if last_author == msg.author.name:
                          if len(msg.mentions) > 0:
                              for mention in msg.mentions:
                                  msg.content.replace("<@!" + str(mention.id) + ">", "@" + mention.name)
                          prefix = prefix + msg.content + "\n"
                      else:
                          if len(msg.mentions) > 0:
                              for mention in msg.mentions:
                                  msg.content.replace("<@!" + str(mention.id) + ">", "@" + mention.name)
                          last_author = msg.author.name
                          prefix = prefix + "\n\n" + msg.author.name + ":\n" + msg.content + "\n"
                  
                  ### Conditions ###
                  if message.content=='!sports':
                    await message.channel.send(generate(message.content,'sports'))
                  elif message.content=='!business':
                    await message.channel.send(generate(message.content,'business'))
                  #elif message.content=='politics':
                  await message.channel.send(generate(message.content,'politics'))
                  
                                               
            else:
              print('Invalid')
client.run('ODQ4ODkzOTc4NTY4MTYzMzc5.YLTQIA.YVBq2h6GS9wHC_RePWvIJT-h1KA')
