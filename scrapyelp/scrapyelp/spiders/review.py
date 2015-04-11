import scrapy
import json 
from scrapyelp.items import ReviewItem
import os

def normalize_whitespace(str):
    import re
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str

class ReviewSpider(scrapy.Spider):
    name = "review"
    allowed_domains = ["yelp.com"]
    
    def __init__(self, URL=None, *args, **kwargs):
        '''Entry is a JSON file that hasa list of the URL to be crawled'''
        if URL:
            json_data=open(os.path.join('/Users/guillaumemiara/Documents/Source/YelpAnalyzer/Temp', URL)) # Open the output from Yelp Search API
            data = json.load(json_data)
            print data    
            super(ReviewSpider, self).__init__(*args, **kwargs)
            self.start_urls = data
        

    def parse(self, response): # Return a dictionary with ID as key and a tuple (rating,content)
        '''Selection of the top box with business info for the page
           Then selection of the reviews information.
           Each parsed item must match the defined Scrapy item

            review_business_name = scrapy.Field()
            review_business_rating = scrapy.Field()
            review_business_reviews_count = scrapy.Field()
            review_business_price_range = scrapy.Field()
            review_business_price_range_detail = scrapy.Field()

            review_content = scrapy.Field()
            review_rating = scrapy.Field()

        '''

        #Business box
        business = response.xpath('.//div[@class="biz-page-header clearfix"]')

        #Business info
        business_name = business.xpath('.//h1[@itemprop="name"]/text()').extract()
        business_rating_meta = business.xpath('.//meta[@itemprop="ratingValue"]')
        business_rating = business_rating_meta.xpath('@content').extract()
        business_reviews_count = business.xpath('.//span[@itemprop="reviewCount"]/text()').extract()
        business_price_range = response.xpath('.//span[@class="business-attribute price-range"]/text()').extract()
        business_price_range_detail = response.xpath('.//dd[@class="nowrap price-description"]/text()').extract()

        #Review info
        reviews = response.xpath('.//div[@class="review-content"]')
        for rev in reviews:

            rating_meta = rev.xpath('.//div[@class="rating-very-large"]')
            rating = float(rating_meta.re('(\d\.\d)')[0])
            content = rev.xpath('.//p[@itemprop="description"]/text()').extract()
            item = ReviewItem()
            item['review_business_name'] = normalize_whitespace(str(business_name[0].encode('ascii', errors='ignore')))
            item['review_business_rating'] = float(business_rating[0])
            item['review_business_reviews_count'] = float(business_reviews_count[0])
            item['review_business_price_range'] = len(business_price_range)
            item['review_business_price_range_detail'] = normalize_whitespace(str(business_price_range_detail[0]))
            item['review_rating'] = rating
            item['review_content']= content[0].encode('ascii', errors='ignore')
            yield item




