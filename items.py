# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyUnsplashItem(scrapy.Item):
    image_url = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    image_path = scrapy.Field() # path to saving the images
    
    
