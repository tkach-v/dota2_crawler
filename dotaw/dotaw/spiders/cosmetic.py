import scrapy
import json
import re

from ..items import DotaCosmeticItem


class CosmeticSpider(scrapy.Spider):
    name = "cosmetic"

    start_urls = ["https://dota2.fandom.com/wiki/Dota_2_Wiki"]

    def start_requests(self):
        with open(r"C:\my_python\tasks\parsers\dota2\dotaw\dotaw\spiders\heroes_links_fandom.json", 'r') as f1:
            heroes = json.load(f1)

        urls = heroes[0]["links"]
        urls = sorted(urls)
        for url in urls:
            yield scrapy.Request(url=url + "?l=english", callback=self.parse)


    def parse(self, response):
        item = DotaCosmeticItem()

        hero = response.css("#firstHeading::text").get()
        cosmetic_labels = response.css(".cosmetic-label").getall()

        cosmetics = []
        for i in cosmetic_labels:
            sel = scrapy.Selector(text=i)

            try:
                url = sel.css("div a img::attr(data-src)").get()

                pattern = re.compile(r"(?<=revision).*")
                new_url = re.sub(pattern, "", url).split('/revision')[0]


                skin = {}
                skin['name'] = sel.css("a::text").get()
                skin['image_url'] = new_url
                cosmetics.append(skin)
            except Exception:
                cosmetics.append([])




        item["hero_name"] = hero.strip()
        item["cosmetics"] = cosmetics


        yield item
