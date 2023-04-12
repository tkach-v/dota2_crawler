import json
import re
import time

import scrapy
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..items import DotaHeroItem


class HeroSpider(scrapy.Spider):
    name = "hero"

    def __init__(self):
        driver_path = r"C:\my_python\tasks\chromedriver.exe"
        self.driver = Chrome(executable_path=driver_path)

    def start_requests(self):
        with open(r"C:\my_python\tasks\parsers\dota2\dotaw\dotaw\spiders\heroes_links.json", 'r') as f1:
            heroes = json.load(f1)

        urls = heroes[0]["links"]
        for url in urls[:2]:
            yield scrapy.Request(url=url + "?l=english", callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)

        # Чекаємо, поки не знайдеться елемент <footer>
        wait = WebDriverWait(self.driver, 100)
        footer = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".rootfooter_RootFooter_H4Gkw")))
        time.sleep(5)
        html = self.driver.page_source

        selector = scrapy.Selector(text=html)

        item = DotaHeroItem()

        primary_stat = selector.css(".heropage_PrimaryStat_3HGWJ::text").get()
        name = selector.css(".heropage_HeroSummary_2jP25 .heropage_HeroName_2IcIu::text").get()
        description_short = selector.css(".heropage_HeroOneLiner_2r7td::text").get()
        description_long_div = selector.css(".heropage_SummaryContainer_2z0_h .heropage_Lore_1FdIS")
        description_long_text = ''.join(description_long_div.xpath('.//text()').getall()).replace('Read Full History',
                                                                                                  '').strip()
        attack_type = selector.css(".heropage_Value_3ce-D::text").get()
        complexity = len(selector.css(".heropage_Filled_2VXnq").getall())

        image_url_small = selector.css(".heropage_Portrait_CR-Bb::attr(src)").get()
        image_url_large = selector.css(".heropage_HeroPortrait_22nJ5 img::attr(src)").get()

        health = selector.css(".heropage_HealthBar_D6gmc .heropage_BarNumberMajor_1KbXK::text").get()
        mana = selector.css(".heropage_ManaBar_1aQk6 .heropage_BarNumberMajor_1KbXK::text").get()

        attributes = selector.css(".heropage_SingleAttributeContainer_1Bhn_").getall()
        for i in range(len(attributes)):
            attr_selector = scrapy.Selector(text=attributes[i])
            if i == 0:
                strength = attr_selector.css(".heropage_AttributeValue_3Gsgg::text").get()
                strength_increase = attr_selector.css(".heropage_AttributeGain_DpX1z::text").get().replace('+',
                                                                                                           '').strip()
            elif i == 1:
                agility = attr_selector.css(".heropage_AttributeValue_3Gsgg::text").get()
                agility_increase = attr_selector.css(".heropage_AttributeGain_DpX1z::text").get().replace('+',
                                                                                                          '').strip()
            else:
                intelligence = attr_selector.css(".heropage_AttributeValue_3Gsgg::text").get()
                intelligence_increase = attr_selector.css(".heropage_AttributeGain_DpX1z::text").get().replace('+',
                                                                                                               '').strip()

        stats_sections = selector.css(".heropage_HeroValuesSection_3ulLB").getall()
        for i in range(len(stats_sections)):
            sec_selector = scrapy.Selector(text=stats_sections[i])
            pattern = r'>\s*([\d/.\-%\s]+)\s*<'

            if i == 0:
                attack_sections = sec_selector.css(".heropage_ValueElement_3783T").getall()
                damage = re.search(pattern, attack_sections[0]).group(1)
                attack_delay = re.search(pattern, attack_sections[1]).group(1)
                attack_range = re.search(pattern, attack_sections[2]).group(1)
                flight_speed = re.search(pattern, attack_sections[3]).group(1)

            elif i == 1:
                defence_sections = sec_selector.css(".heropage_ValueElement_3783T").getall()
                armor = re.search(pattern, defence_sections[0]).group(1)
                magic_resistance = re.search(pattern, defence_sections[1]).group(1)


            else:
                mobility_sections = sec_selector.css(".heropage_ValueElement_3783T").getall()
                move_speed = re.search(pattern, mobility_sections[0]).group(1)
                turn_speed = re.search(pattern, mobility_sections[1]).group(1)
                vision = re.search(pattern, mobility_sections[2]).group(1)

        item["primary_stat"] = primary_stat
        item["name"] = name
        item["description_short"] = description_short
        item["description_long"] = description_long_text
        item["attack_type"] = attack_type
        item["complexity"] = complexity
        item["image_url_small"] = image_url_small
        item["image_url_large"] = image_url_large
        item["health"] = health
        item["mana"] = mana
        item["strength"] = strength
        item["strength_increase"] = strength_increase
        item["agility"] = agility
        item["agility_increase"] = agility_increase
        item["intelligence"] = intelligence
        item["intelligence_increase"] = intelligence_increase
        item["damage"] = damage
        item["attack_delay"] = attack_delay
        item["attack_range"] = attack_range
        item["flight_speed"] = flight_speed
        item["armor"] = armor
        item["magic_resistance"] = magic_resistance
        item["move_speed"] = move_speed
        item["turn_speed"] = turn_speed
        item["vision"] = vision

        yield item

    def __del__(self):
        self.driver.quit()
