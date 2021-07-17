import praw
import time
# load tokenizer
# read dataframe of comments and comment_ids
# initialize subreddit

def authenticate_user(reddit_username, reddit_password,
                      reddit_app_client_id, reddit_app_client_secret):
    ''' Authenticates user with the PRAW library '''

    reddit = praw.Reddit(client_id=reddit_app_client_id,
                         client_secret=reddit_app_client_secret,
                         username=reddit_username,
                         password=reddit_password,
                         user_agent = 'bot by /yugaljain1999' )
    return reddit
   # return reddit.user.me() if reddit.user.me() == reddit_username else None
def reply_comment(reddit,comment_df):

    for ids,rows in comment_df.iterrows():
        result = reddit.comment(id = rows['comment_id'])
        
        
        if rows['reply']=='||' or rows['reply']=='.||' or rows['reply']==',||' or rows['reply']=='?||' or rows['reply']=='':
          continue
        print('Prompt',rows['comments'])
        
        if len(rows['reply'])>=1:

          if rows['reply']!='||' or rows['reply']!='':
            t= rows['reply']
            ch = ['.||','?||',',||','||']
            for c in ch:
              t = t.replace(c,"")
            if re.search('[a-zA-Z]',t):
              result.reply(t)
              print('REPLY',rows['reply'])
              time.sleep(600)
          else:
            continue
        else:
          continue
          
# Delete useless reddit comments


def delete_new_comments(redditor):
    redditor = redditor.user.me()
    for comment in redditor.comments.new(limit=None):
        if comment.body=='||' or comment.body=='nan' or comment.score<1:
            #comment.edit('-')
            comment.delete()
