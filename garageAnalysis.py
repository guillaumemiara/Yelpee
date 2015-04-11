import os
import sys


#1. Set working path to scrapy directory
os.chdir("scrapyelp")

#2. Run the spider to collect the reviews
os.system( "scrapy crawl garageSale -o ../GarageTemp/garageSale.jsonlines ")
os.system( "scrapy crawl garageRent -o ../GarageTemp/garageRent.jsonlines ")
print "Crawling done"
#3. Go back to main dir
os.chdir("..")

#4. Run the analysis on the review & return result to Output
os.system("python runGarageAnalysis.py " )
print "Analysis done"

#5. Delete content in Temp folder
#os.system("rm -rfv Temp/*")
