__author__ = 'guillaumemiara'

import scrapy
import json
from scrapyelp.items import GarageRentItem
import os
import re

def normalize_whitespace(str):
    import re
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str

class GarageRentSpider(scrapy.Spider):
    name = "garageRent"
    allowed_domains = ["pap.fr"]
    start_urls = ('http://www.pap.fr/annonce/locations-parkings-paris-75-g439-200-annonces-par-page',)

    def parse(self, response): # Return a dictionary with ID as key and a tuple (rating,content)
        '''Selection of the garage sale info
           garage_rent_price = scrapy.Field()
           garage_rent_location = scrapy.Field()
           garage_rent_description = scrapy.Field()
        '''

        #List box

        box_listing = response.xpath('//ul[@class="search-results-list"]')

        for garage_annonce in box_listing.xpath('.//li[@class="annonce"]'):

            garage_rent_price = garage_annonce.xpath('.//span[@class="prix"]/text()').extract()

            garage_meta= garage_annonce.xpath('.//div[@class="description clearfix"]')
            garage_rent_location = garage_meta.xpath('.//strong/text()').extract()
            tosearch = garage_rent_location[0].encode('ascii', errors='ignore')
            extracted_location = re.findall(r"\D(\d{5})\D",tosearch)[0]

            garage_rent_description = garage_meta.xpath('.//p/text()').extract()

            item = GarageRentItem()
            if garage_rent_price:
                item['garage_rent_price']= float(garage_rent_price[0].encode('ascii', errors='ignore'))
            else:
                item['garage_rent_price']=float(0)
            item['garage_rent_location']= float(extracted_location)
            item['garage_rent_description']= garage_rent_description[1].encode('ascii', errors='ignore')
            item['annonce_type'] = 'rent'
            yield item





