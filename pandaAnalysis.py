__author__ = 'guillaumemiara'


import json
import os
import pandas as pd
import matplotlib.pyplot as plt

import math
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from collections import Counter
import numpy as np
from pandas import DataFrame, Series
import matplotlib.pyplot as plt


# AFINN-111 is as of June 2011 the most recent version of AFINN
filenameAFINN = 'AFINN-111.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [
            ws.strip().split('\t') for ws in open(filenameAFINN) ]))

# Word splitter pattern
pattern_split = re.compile(r"\W+")

def sentiment(text):
    """
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence.
    """
    words = pattern_split.split(text.lower())
    sentiments = map(lambda word: afinn.get(word, 0), words)
    if sentiments:
        # How should you weight the individual word sentiments?
        # You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
        sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))

    else:
        sentiment = 0
    return sentiment

'''
For large file, it is better to open with json lines
'''

data = []

with open(os.path.join('Temp','reviews.jsonlines'),'r') as f:
    for line in f:
        data.append(json.loads(line))


biz = [ biz['review_business_name'] for biz in data if 'review_business_name' in biz]

df = DataFrame(data)

def calculate(l):
    s = sentiment(l['review_content'])
    return pd.Series(dict(sentiment_rating= s))

df = df.merge(df.apply(calculate, axis=1), left_index=True, right_index=True)

df.plot(x = 'review_rating',y = 'sentiment_rating', kind = 'hexbin', gridsize=25);

plt.show()
'''
for index, row in df.iterrows():
    print row['']
'''

