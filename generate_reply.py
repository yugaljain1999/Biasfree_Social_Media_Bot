import re
import torch
import pandas as pd
def generate_reply(model,device,comment_df,gedi_model,tokenizer,multi_code=None):
    texts = []
    for comment in comment_df['comments']:
        encoded_prompts = tokenizer.encode(comment)
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
                                                do_sample=False,
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
        text = text[len(comment):]
        text = text.replace("||","")
        text = re.sub("||","",text)
        text =  re.sub("||","",text)
        text = re.sub('<|endoftext|>','',text)
        text = text.replace('<|endoftext|>','')
        
        
        #print('reply_gen',text)
        texts.append(text)

    texts = pd.Series(texts)
    df_india = pd.DataFrame({'comment_id':pd.Series(comment_df['comment_id']),'comments':pd.Series(comment_df['comments']),'reply':pd.Series(texts)})
    df_india.to_csv('comment_reply_.csv')
    return df_india