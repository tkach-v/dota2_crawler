# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DotaHeroItem(scrapy.Item):
    primary_stat = scrapy.Field()
    name = scrapy.Field()
    description_short = scrapy.Field()
    description_long = scrapy.Field()
    attack_type = scrapy.Field()
    complexity = scrapy.Field()
    image_url_small = scrapy.Field()
    image_url_large = scrapy.Field()
    health = scrapy.Field()
    mana = scrapy.Field()

    # attributes
    strength = scrapy.Field()
    strength_increase = scrapy.Field()
    agility = scrapy.Field()
    agility_increase = scrapy.Field()
    intelligence = scrapy.Field()
    intelligence_increase = scrapy.Field()

    # attack
    damage = scrapy.Field()
    attack_delay = scrapy.Field()
    attack_range = scrapy.Field()
    flight_speed = scrapy.Field()

    # defence
    armor = scrapy.Field()
    magic_resistance = scrapy.Field()

    # mobility
    move_speed = scrapy.Field()
    turn_speed = scrapy.Field()
    vision = scrapy.Field()

    # talent_tree
    left_10 = scrapy.Field()
    right_10 = scrapy.Field()
    left_15 = scrapy.Field()
    right_15 = scrapy.Field()
    left_20 = scrapy.Field()
    right_20 = scrapy.Field()
    left_25 = scrapy.Field()
    right_25 = scrapy.Field()


class DotaAbilityItem(scrapy.Item):
    hero_name = scrapy.Field()
    abilities = scrapy.Field()


class DotaCosmeticItem(scrapy.Item):
    hero_name = scrapy.Field()
    cosmetics = scrapy.Field()
