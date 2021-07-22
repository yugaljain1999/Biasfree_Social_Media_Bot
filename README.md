# Social Media Unbiased Reply Bot

Datasets Used
* Jigsaw Toxic Comment Classification
* AG-News Topic Classification Dataset

Trained Weights-
Download pytorch pretrained weights and put it in parent folder.

* Trained sentiment model weights - https://drive.google.com/file/d/1pRRO8dvGi9nr2hwuKXoXidqmAdXvK5Ks/view?usp=sharing

* Trained topic model detoxify weights - https://www.dropbox.com/s/en5vl7ssirbbxzx/AG_news_gedi_model_detoxify.pth?dl=0

Run Discord bot-
* Replace discord token in line 124 in discord_reply.py with yours bot token which you can generate through discord developers applications.

* Then run
```
python discord_reply.py
```
* Try out in colab
https://colab.research.google.com/drive/1Y4KQmljT7yiezs5HZuIbsn1yhaOec86w?usp=sharing

Sample Outputs-

![alt text](https://github.com/yugaljain1999/biasfree_bot_GeDi/blob/main/discord_bot_output.png)

References-
* https://arxiv.org/abs/2009.06367
* https://github.com/salesforce/GeDi
