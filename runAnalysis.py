
import os
import sys
import json
from textblob import TextBlob
import operator
from collections import Counter
from textblob.classifiers import NaiveBayesClassifier

output_file = sys.argv[1]

output_filename = str(output_file)+'.json'

print output_filename


keys_to_remove = ['i','of','the','and','a','to','was','u','it','is','for','s','in','you','but','that','so','this','with','on','have','be','they','we','can','n\'t','my','there','all','are','up','just','not','if','their','had','order','place','do','an','go','m','get','me','xa0','here','more','because','what','from','xa0i','your','or','still','would','has','as','at','were','one','got','know','will','did','came','\'ll','only','ve','ever','though','also','which','about','tried','some','around','other','say','by','make','after','no','even','try','much','ll','could','been','over','too','re','next','u\'i','eat','food','than','them','he','xa0the','us','our','menu','back','when','u\'the','ordered','bit','who','two','three','want','think','before','come','made','how','way','then','going']

 
def countWords(review):
    text = TextBlob(review)
    D =  text.word_counts
    sorted_D = dict(sorted(D.items(), key=operator.itemgetter(1), reverse=True))
    return sorted_D

def format_rev(rev):
    review = rev['review_content']
    rating = rev['review_rating']
    classification = ''
    if rating >2:
        classification = 'pos'
    if rating <2:
       classification = 'neg'
    return (review , classification)

def format_rev2(rev):
    review = rev['review_content']
    classification = rev['review_rating']
    return (review , classification)


def run_countwords():
    json_data=open(os.path.join('Temp','reviews.json'),'r') # Open the output from Yelp Webcrawling
    data = json.load(json_data)
    D = Counter({})
    for rev in data:
        review = rev['review_content']
        C = Counter(countWords(review))
        D =  D + C

    # D = {key: value for key, value in D.items() if key is not in value_to_remove}
    for key in keys_to_remove:
        del D[key]
    
    final = sorted(D.items(), key=operator.itemgetter(1), reverse=True)[:50]

    output = [dict(word= n[0], count = n[1]) for n in final]

    with open(os.path.join('output', output_filename), 'w') as outfile:
      json.dump(output, outfile)

def run_classify():
    json_data=open(os.path.join('Temp','reviews.json'),'r') # Open the output from Yelp Webcrawling
    data = json.load(json_data)
    
    train = []
    for rev in data:
        couple = format_rev(rev)
        train.append(couple)

    cl = NaiveBayesClassifier(train)
    print "We expect to see something positive here: " , cl.classify("This place was amazing!")
    print "We expect to see something negative here: " , cl.classify("It was a nightmare, the food was disgusting and I will never go back. Terrible. Bad")
    print cl.labels()


def run_classify2():
    json_data=open(os.path.join('Temp','reviews.json'),'r') # Open the output from Yelp Webcrawling
    data = json.load(json_data)
    
    train = []
    for rev in data:
        couple = format_rev2(rev)
        train.append(couple)

    cl = NaiveBayesClassifier(train)
    print "We expect to see something positive here: " , cl.classify("This place was amazing!")
    print "We expect to see something negative here: " , cl.classify("Eek! Methinks not is spot on. I tried really hard to like this place, since it's fairly close to where I live and I could just walk there. However, the handful of times that I've visited this place, whether it be in the early mornings after my roggings (run/jogs) or afternoon coffee cravings, it has always been so disappointing. Sadly, not once have I been satisfied with this place. And yet, I've given them so many chances.The main reason I have been utterly disappointed with this place is due to the lack of care and respect the employees have for it and their customers. The workers here are lazy, rude, unapologetic and just plain out of it. 4 out of 5 times, the same guy will miss my drink. I only order a small coffee or iced chai. He always gets it wrong; making my chai hot or my coffee iced or mixing up the sizes. Never apologizes and instead just dismisses it as if I were the person that ordered wrong. The service is slow. On one account, I was there waiting and waiting for some service (a coffee!) while two workers were just diddle daddling around. No one was there. Except me. They heard me but continued to ignore me until I had to call out to them and ask for help. Incredible! And another observation would be, why are there always flies around their pies? The food here is meh and really nothing to rave about. The coffee too. Drinks are not more better than anywhere else and prices are about the same-$3.50 for an iced chai poured from a box. With that said, I usually and hardly write bad reviews but with this place, it's been accumulating minus points so it's only fair to share my two cents. It's a simple, local neighborhood place but in my opinion, there's a bunch of coffee spots that are all within walking distance so save yourself the trip and have your coffee elsewhere.")
    print "We expect to see something negative here: " , cl.classify("Nothing good to remember of this place. They forgot part of my order... The coffee wasn't even nice.Sorry, wouldn't come back.")
    print "We expect to see something negative here: " , cl.classify("This place has pretty bad service and bad specialty drinks. I ordered a chai latte that was $5 w almond milk. It tasted like really really sweet almond milk... No chai flavor at all. I told them and they said well sorry. You can buy another drink if you want. No I wanted a drink that was made right in the first place.Don't go here unless you have too.")
    print "We expect to see something negative here: " , cl.classify("The coffee here is above average, and the food is generally pretty good. But the place is always a mess when I go there. There are frequently coffee spills and napkins on the floor and flies buzzing all over the place. The staff seems disinterested and the service is consistently slow. I prefer to get my coffee or food to go because the ambience is unpleasant.")
    print cl.labels()

def stat():
    json_data=open(os.path.join('Temp','reviews.json'),'r') # Open the output from Yelp Webcrawling
    data = json.load(json_data)
    c1 = 0
    c2 = 0
    c3 = 0
    c4 = 0
    c5 = 0

    for rev in data:
        rating = rev['review_rating']
        if rating == 1.0:
            c1 = c1+1
        elif rating == 2.0:
            c2= c2+1
        elif rating == 3.0:
            c3 = c3+1
        elif rating == 4.0:
            c4 = c4+1
        elif rating == 5.0:
            c5 = c5+1

    print "Total number or reviews: %d" %(c1+c2+c3+c4+c5)
    print "The number of reviews of rating 1: %d , 2: %d , 3: %d , 4: %d, 5: %d " % (c1, c2, c3, c4, c5)

if __name__ == '__main__':
  run_countwords()
  stat()
  #run_classify2()








