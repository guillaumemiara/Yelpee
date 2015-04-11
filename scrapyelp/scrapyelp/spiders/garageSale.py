__author__ = 'guillaumemiara'

import scrapy
import json
from scrapyelp.items import GarageSaleItem
import os
import re

def normalize_whitespace(str):
    import re
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str

class GarageSaleSpider(scrapy.Spider):
    name = "garageSale"
    allowed_domains = ["pap.fr"]
    start_urls = ('http://www.pap.fr/annonce/garage-parkings-paris-75-g439-200-annonces-par-page',)

    def parse(self, response): # Return a dictionary with ID as key and a tuple (rating,content)
        '''Selection of the garage sale info
           garage_sale_price = scrapy.Field()
           garage_sale_location = scrapy.Field()
           garage_sale_description = scrapy.Field()
        '''

        #List box

        box_listing = response.xpath('//ul[@class="search-results-list"]')

        for garage_annonce in box_listing.xpath('.//li[@class="annonce"]'):

            garage_sale_price = garage_annonce.xpath('.//span[@class="prix"]/text()').extract()

            garage_meta= garage_annonce.xpath('.//div[@class="description clearfix"]')
            garage_sale_location = garage_meta.xpath('.//strong/text()').extract()
            tosearch = garage_sale_location[0].encode('ascii', errors='ignore')
            extracted_location = re.findall(r"\D(\d{5})\D",tosearch)[0]

            garage_sale_description = garage_meta.xpath('.//p/text()').extract()

            item = GarageSaleItem()
            if garage_sale_price:
                item['garage_sale_price']= float(garage_sale_price[0].encode('ascii', errors='ignore'))
            else:
                item['garage_sale_price']=float(0)
            item['garage_sale_location']= float(extracted_location)
            item['garage_sale_description']= garage_sale_description[1].encode('ascii', errors='ignore')
            item['annonce_type'] = 'sale'
            yield item





