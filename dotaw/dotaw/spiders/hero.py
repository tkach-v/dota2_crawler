import scrapy
# from selenium.webdriver import Chrome
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from ..items import DotawItem

class HeroSpider(scrapy.Spider):
    name = "hero"
    allowed_domains = ["test.com"]
    start_urls = [
        "file:///C:/my_python/tasks/parsers/dota2/output.html"
    ]

    def parse(self, response):
        item = DotawItem()
        links = []
        for link in response.css(".herogridpage_HeroIcon_7szOn::attr(href)").getall():
            links.append("https://www.dota2.com" + link)
        yield {"links": links}

