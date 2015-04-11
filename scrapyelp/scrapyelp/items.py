# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewItem(scrapy.Item):
    # define the fields for your item here like:
    '''For each review, we will retrieve information - relative to the business & relative to the review'''
    review_business_name = scrapy.Field()
    review_business_rating = scrapy.Field()
    review_business_reviews_count = scrapy.Field()
    review_business_number_rating = scrapy.Field()
    review_business_price_range = scrapy.Field()
    review_business_price_range_detail = scrapy.Field()

    review_content = scrapy.Field()
    review_rating = scrapy.Field()

    pass

class GarageSaleItem(scrapy.Item):
    # define the fields for your item here like:
    '''For each review, we will retrieve information - relative to the business & relative to the review'''
    garage_sale_price = scrapy.Field()
    garage_sale_location = scrapy.Field()
    garage_sale_description = scrapy.Field()
    annonce_type = scrapy.Field()

    pass

class GarageRentItem(scrapy.Item):
    # define the fields for your item here like:
    '''For each review, we will retrieve information - relative to the business & relative to the review'''
    garage_rent_price = scrapy.Field()
    garage_rent_location = scrapy.Field()
    garage_rent_description = scrapy.Field()
    annonce_type = scrapy.Field()


    pass
