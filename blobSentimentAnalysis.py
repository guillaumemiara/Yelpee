__author__ = 'guillaumemiara'


import json
import os
import pandas as pd
from textblob import TextBlob
from collections import Counter
import numpy as np
from pandas import DataFrame, Series
import matplotlib.pyplot as plt



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
    text = TextBlob(l['review_content'])
    s = text.sentiment.polarity
    p = text.sentiment.subjectivity
    return pd.Series(dict(sentiment_rating= s,sentiment_rating_polarity = p))

df = df.merge(df.apply(calculate, axis=1), left_index=True, right_index=True)

print "Sentiment rating grouped by rating"
print 50*'-'
print df.groupby(['review_rating']).mean()['sentiment_rating']

print "Sentiment rating grouped by polarity"
print 50*'-'
print df.groupby(['review_rating']).mean()['sentiment_rating_polarity']

df.plot(x = 'review_rating',y = 'sentiment_rating_polarity', kind = 'hexbin', gridsize=25);

plt.show()

'''
df.plot(x = 'review_rating',y = 'sentiment_rating', kind = 'hexbin', gridsize=25);

plt.show()
'''


