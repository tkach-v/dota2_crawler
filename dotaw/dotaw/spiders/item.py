import json
import re

import scrapy

from ..items import DotaItemItem


class ItemSpider(scrapy.Spider):
    name = "item"

    start_urls = ["https://dota2.fandom.com/wiki/Dota_2_Wiki"]

    def start_requests(self):
        with open(r"C:\my_python\tasks\parsers\dota2\dotaw\dotaw\spiders\items_list.json", 'r') as f1:
            items = json.load(f1)

        urls = items[0]["links"]
        for url in urls:
            yield scrapy.Request(url="https://dota2.fandom.com" + url, callback=self.parse)

    def parse(self, response):
        try:
            item = DotaItemItem()

            name = response.css(".page-header__title::text").get().strip()

            image_url = response.css("#itemmainimage img::attr(data-src)").get()

            description = re.sub('<[^<]+?>', '', response.css("#pageTabber+ p").extract()[0]).strip()
            lore_description = response.css(".infobox > tbody > tr:nth-child(3) td::text").get().strip()

            type_specific = response.css(".infobox table tr:nth-child(1) th span::text").get()
            if type_specific.startswith("Tier"):
                type_global = "Neutral"
            else:
                type_global = "Basics"

            trs = response.css(".infobox tr").getall()

            cost = None
            sell_value = None
            bonus = None
            shareable = None
            disassemble = None
            availability = None

            for i in range(len(trs)):
                sel = scrapy.Selector(text=trs[i])

                if sel.xpath('.//*[contains(text(), "Cost")]'):
                    cost = sel.css("b::text").get()
                    if type(cost) == str:
                        cost = cost.strip()
                    if not cost:
                        cost = None

                if sel.xpath('.//*[contains(text(), "Sell")]'):
                    sell_value = sel.css("b::text").get()
                    if type(cost) == str:
                        cost = cost.strip()
                    if not sell_value:
                        cost = None

                if sel.xpath('.//*[contains(text(), "Bonus")]'):
                    bonus = re.sub('<[^<]+?>', '', sel.css("td:last-child").extract()[0]).strip()
                    if not bonus:
                        bonus = None

                if sel.xpath('.//*[contains(text(), "Shareable")]'):
                    shareable = sel.css("img::attr(alt)").get()
                    if not shareable:
                        shareable = None

                if sel.xpath('.//*[contains(text(), "Disassemble")]'):
                    disassemble = sel.css("img::attr(alt)").get()
                    if not disassemble:
                        disassemble = None

                if sel.xpath('.//*[contains(text(), "Availability")]'):
                    availability = re.sub('<.*?>', '', sel.css("td:last-child").extract()[0])
                    availability = re.sub('\s*game-time', '', availability).strip()
                    if not availability:
                        availability = None

                if sel.xpath('.//*[contains(text(), "Recipe")]'):
                    recipe = []
                    sel = scrapy.Selector(text=trs[i+1])
                    links = sel.css("a").getall()

                    for link in links:
                        sel1 = scrapy.Selector(text=link)
                        href = sel1.css("::attr(href)").get()
                        if href != response.request.url[24:]:
                            result = sel1.css("::attr(title)").get()
                            result = re.sub(r'\s*\(\d+\)', '', result)
                            recipe.append(result)

            item["name"] = name
            item["image_url"] = image_url
            item["description"] = description
            item["lore_description"] = lore_description
            item["type_global"] = type_global
            item["type_specific"] = type_specific
            item["cost"] = cost
            item["sell_value"] = sell_value
            item["bonus"] = bonus
            item["shareable"] = shareable
            item["disassemble"] = disassemble
            item["availability"] = availability
            item["recipe"] = recipe

            yield item

        except:
            item = DotaItemItem()
            name = response.css(".page-header__title::text").get().strip()
            item['name'] = name
            yield item
