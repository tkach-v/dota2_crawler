import json
import re

import scrapy

from ..items import DotaItemAbilityItem


class ItemAbilitiesSpider(scrapy.Spider):
    name = "item_abilities"
    start_urls = ["https://dota2.fandom.com/wiki/Dota_2_Wiki"]

    def start_requests(self):
        with open(r"C:\my_python\tasks\parsers\dota2\dotaw\dotaw\spiders\items_list.json", 'r') as f1:
            items = json.load(f1)

        urls = items[0]["links"]
        for url in urls:
            yield scrapy.Request(url="https://dota2.fandom.com" + url, callback=self.parse)

    def parse(self, response):
        try:
            item = DotaItemAbilityItem()

            item_name = response.css(".page-header__title span::text").get().strip()

            abilities = response.css(".ability-background").getall()
            result_list = []

            for ability in abilities:
                result_item = {}
                sel = scrapy.Selector(text=ability)

                name = sel.css("div:first-child > div span::text").get()

                ab = str(sel.css(".ability-description > *:nth-child(1) > *:nth-child(1)").extract())
                ab = re.sub(r'<.*?>', '', ab)
                ab = ab[9:-2]

                affects = str(sel.css(".ability-description > *:nth-child(1) > *:nth-child(2)").extract())
                affects = re.sub(r'<.*?>', '', affects)
                affects = affects[9:-2]

                damage = str(sel.css(".ability-description > *:nth-child(1) > *:nth-child(3)").extract())
                damage = re.sub(r'<.*?>', '', damage)
                damage = damage[8:-2]

                description = str(sel.css(".ability-description > *:nth-child(2)").extract())
                description = re.sub(r'<div[^>]*>', '', description)
                description = re.sub(r'</div>', '', description)
                description = description[2:-2]

                details = {}
                detail_list = sel.css("div:first-child > *:nth-child(3) > div").getall()
                cooldown = None
                manacost = None
                for div in detail_list:
                    sel1 = scrapy.Selector(text=div)

                    if "font-size:98%" in str(div):
                        details[sel1.css("b::text").get()] = sel1.css("span::text").get()
                    elif "display:inline-block; margin:8px 0px 0px 20px; font-size:95%" in str(div):
                        try:
                            cooldown = sel1.css(
                                "div > div > div:nth-child(1) > div > div:last-child::text").get().strip()
                            manacost = sel1.css("div > div > div:nth-child(2) > div:last-child::text").get().strip()
                        except:
                            cooldown = "Change\n"
                            manacost = "Change\n"

                result_item["name"] = name
                result_item["ability"] = ab
                result_item["affects"] = affects
                result_item["damage"] = damage
                result_item["description"] = description
                result_item["details"] = details
                result_item["cooldown"] = cooldown
                result_item["manacost"] = manacost

                result_list.append(result_item)

            item['item_name'] = item_name
            item['abilities'] = result_list

            yield item

        except:
            item = DotaItemAbilityItem()
            item_name = response.css(".page-header__title span::text").get().strip()
            item['item_name'] = item_name
            item['abilities'] = ["Error here"]
            yield item
