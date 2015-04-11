import os
import sys

term = sys.argv[1]
loc = sys.argv[2]
lim = sys.argv[3]
searchterm = sys.argv[4]


searchterm = "python YelpSearchApi.py " + term + " " + loc+ " " + lim + " " + searchterm
output_file = term + loc+ "_" + lim 

#1. Run the script to use Yelp Search Api and Retreive reviews 
os.system(searchterm)
# Store results as a json in the Temp folder - they will be used as scrapy input
print "Search done"

#2. Set working path to scrapy directory
os.chdir("scrapyelp")

#3. Run the spider to collect the reviews
os.system( "scrapy crawl review -o ../Temp/reviews.jsonlines -a URL='URLlist.json' ")
print "Crawling done"
#4. Go back to main dir
os.chdir("..")

#5. Run the analysis on the review & return result to Output
os.system("python runAnalysis.py " + output_file )
print "Analysis done"

#6. Delete content in Temp folder
#os.system("rm -rfv Temp/*")
