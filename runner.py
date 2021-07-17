from transformers import GPT2Tokenizer
import torch
import numpy as np
import re
import praw
from extract_comments import extract_comments
from reply import authenticate_user
from reply import reply_comment
from reply import delete_new_comments
from generate_reply import generate_reply

from main import *
if torch.cuda.is_available():
  device = torch.device('cuda')
secondary_code = 'positive'
subreddit = 'Depression'
model,gedi_model = GeDi()
tokenizer = GPT2Tokenizer.from_pretrained('gpt2',do_lower_case=False)
multi_code = tokenizer.encode(secondary_code)
reddit = authenticate_user('unbiasreply','Unbiasreply','K60Bge5rm-gelw','aY-vPWZHQXzZR44qCr8QYHGIp8U')
def main():
  # extract comments
  comments_df = extract_comments(reddit=reddit,subreddit=subreddit)
  comments = comments_df['comments']
  comment_ids = comments_df['comment_id']
  print('---------------')
  # generating replies from comments
  comments_replies = generate_reply(model,device,comment_df=comments_df,gedi_model=gedi_model,
                                      tokenizer=tokenizer,multi_code = multi_code)
  # reply to comments on reddit
  reply_comment(reddit=reddit,comment_df=comments_replies)
  # To delete recent comments- call below function
  # delete_new_comments(reddit)

if __name__=='__main__':
    while True :
        main()
        time.sleep(5)