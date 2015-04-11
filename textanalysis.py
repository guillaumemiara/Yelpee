from textblob import TextBlob

def format(rev):
    review = rev['review_content']
    rating = rev['review_rating']
    classification = ''
    if rating >2:
       classification = 'pos'
    if rating <= 2:
       classification = 'neg'
    return (review , classification)
