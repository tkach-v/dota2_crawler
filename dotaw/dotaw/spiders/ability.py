import json
import time

import scrapy
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..items import DotaAbilityItem


class AbilitySpider(scrapy.Spider):
    name = "ability"

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
        wait = WebDriverWait(self.driver, 10)
        footer = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".rootfooter_RootFooter_H4Gkw")))
        time.sleep(4)
        html = self.driver.page_source

        selector = scrapy.Selector(text=html)

        item = DotaAbilityItem()

        hero_name = selector.css(".heropage_HeroSummary_2jP25 .heropage_HeroName_2IcIu::text").get()
        abilities_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".heropage_AbilitySelector_1vjw5 .heropage_AbilitySelectable_3Chop")

        item["hero_name"] = hero_name

        abilities = []
        for i in range(len(abilities_buttons)):
            abilities_buttons[i].click()

            html_clicked = self.driver.page_source
            sel = scrapy.Selector(text=html_clicked)

            ability = {}
            name = sel.css(".heropage_AbilityName_1rBGH::text").get()

            # Обираємо лише елемент з класом heropage_AbilityDesc_CjmI9
            ability_div = sel.css('.heropage_AbilityDesc_CjmI9')
            # Отримуємо список рядків з вибраного елемента, включаючи теги br
            ability_text_list = ability_div.css('*::text').getall()
            # Об'єднуємо рядки в один рядок
            description = '<br><br>'.join(ability_text_list)

            image_url = sel.css(".heropage_AbilityImage_171zq::attr(src)").get()
            ab_type = sel.css(".heropage_AghType_1RDBb::text").get()

            general_values = sel.css(".heropage_DetailsValues_25_Ud .heropage_ValueElement_3783T").getall()
            ab_generic = {}
            for i in general_values:
                sel = scrapy.Selector(text=i)
                ab_generic[sel.css("::text").get()] = sel.css(".heropage_ValueValue_1gAlz::text").get(default='') or sel.css(".heropage_ValueValue_1gAlz span::text").get()

            ab_specific = {}


            ability["name"] = name
            ability["description"] = description
            ability["image_url"] = image_url
            ability["type"] = ab_type
            ability["generic_details"] = ab_generic
            ability["specific_details"] = ab_specific
            # ability["Ability"] = general_ability
            # ability["Affects"] = general_affects
            # ability["Damage Type"] = general_damage_type
            # ability["Pierces Spell Immunity"] = general_pierces_spell_immunity
            # ability["Dispellable"] = general_dispellable


            abilities.append(ability)

        item["abilities"] = abilities
        yield item

    def __del__(self):
        self.driver.quit()
