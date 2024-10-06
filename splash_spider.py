import scrapy
from scrapy_unsplash.items import ScrapyUnsplashItem
from scrapy_unsplash import SplashRequest


class SplashSpider(scrapy.Spider):
    name = "splash_spider"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute', args={'lua_source': self.script})

    def parse(self, response):
        category_links = response.css("a[href*='/s/']:not([href*='sitemap'])::attr(href)").getall()
        for link in category_links: 
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        category_name = response.css("h1::text").get()
        image_blocks = response.css("figure a[href*='/photos/']")

        for block in image_blocks: 
            image_srcset = block.css("img::attr(srcset)").get()
            if image_srcset:
                image_url = image_srcset.split(",")[-1].split(" ")[0]
            else:
                image_url = None

            title = block.css("img::attr(alt)").get()

            item = ScrapyUnsplashItem(
                image_url=image_url,
                title=title,
                category=category_name
            )

            yield item 

        
        next_page = response.css("a[href*='?page=']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_category)

