# Script that takes in entry search parameters for a YelpSearch and return as an output a json file with the results of that search

import oauth2 as oauth
import urllib2 as urllib
import sys
import json
import os

term = sys.argv[1]
loc = sys.argv[2]
lim = sys.argv[3]
type_search = sys.argv[4]


def interpret_search(search,url):
    if search == "date_asc":
        return [url + "?sort_by=date_asc"]
    if search == "date_desc":
        return [url + "?sort_by=date_desc"]
    if search == "date_both":
        return [url + "?sort_by=date_asc"]+ [url + "?sort_by=date_desc"]
    if search == "rating_asc":
        return [url + "?sort_by=rating_asc"]
    if search == "rating_desc":
        return [url + "?sort_by=rating_desc"]
    if search == "rating_both":
        return [url + "?sort_by=rating_asc"]+ [url + "?sort_by=rating_desc"]
    if search == "date_rating_both" or "rating_date_both":
        return [url + "?sort_by=date_asc"]+ [url + "?sort_by=date_desc"]+[url + "?sort_by=rating_asc"]+ [url + "?sort_by=rating_desc"]


URL = 'http://api.yelp.com/v2/search?term=' + term + '&location=' + loc + '&limit=' + lim 


api_key = ''
api_secret = ''
access_token_key = ''
access_token_secret = ''

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)



'''
Construct, sign, and open a yelp request
using the hard-coded credentials above.
'''


def yelpreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():

  url = URL
  parameters = []
  response = yelpreq(url, "GET", parameters)

  text = json.loads(response.read())

  with open(os.path.join('Temp', 'searchResults.json'), 'w') as outfile:
      json.dump(text, outfile)


def buildListBusinessURL():
    # function to build a list of business URLs from a json
    json_data=open(os.path.join('Temp', 'searchResults.json')) # Open the output from YelpSearch
    data = json.load(json_data)
    businesses = data['businesses']

    ls = []
    for biz in businesses:
        ls = ls + interpret_search(type_search, biz['url'])
        print interpret_search(type_search, biz['url'])
    with open(os.path.join('Temp', 'URLlist.json'), 'w') as outfile:
      json.dump(ls, outfile)


if __name__ == '__main__':
    fetchsamples()
    buildListBusinessURL()




