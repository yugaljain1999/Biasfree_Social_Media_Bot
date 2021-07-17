import re
import pandas as pd
comment_ids = []
prompts = []
def extract_comments(reddit,subreddit):
    # Adding multi-subreddits support
    global previous_id
    previous_id = "0"
    
    for results in reddit.subreddit(subreddit).comments(limit=100):
        #global previous_id
        #print('results.author.name)
        if results.author.name!=reddit.user.me():
                
            body = results.body
            body = re.sub(r'^https?:\/\/.*[\r\n]*', '', body, flags=re.MULTILINE)
            RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
            body = RE_EMOJI.sub(r'', body)
            if body == '':
                continue
            comment_id = results.id
            if comment_id == previous_id:
                    print('error')
            if re.search('r/spook_irl',body):
              continue
            else:
              #if len(args.prompt)>0:#   break #if args.prompt=="q":#   break
              body = body.replace('||','')
              #print('prompt',body)
              previous_id = comment_id
              comment_ids.append(comment_id)
              prompts.append(body)
          #texts.append(text)
    df = pd.DataFrame({'comment_id':pd.Series(comment_ids),'comments':pd.Series(prompts)})
    return df
            