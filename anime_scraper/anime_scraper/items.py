# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join, Compose
from scrapy.loader import ItemLoader
import re

class Anime(scrapy.Item):

    # Identification fields
    id = scrapy.Field()
    original_title = scrapy.Field()
    english_title = scrapy.Field()
    japanese_title = scrapy.Field()
    synonyms = scrapy.Field()

    # Additional informations
    type = scrapy.Field()
    episodes_number = scrapy.Field()
    status = scrapy.Field()
    airing_date = scrapy.Field()
    premiered_date = scrapy.Field()
    demographic = scrapy.Field()
    broadcast_date = scrapy.Field()
    producers = scrapy.Field()
    licensors = scrapy.Field()
    studios = scrapy.Field()
    source = scrapy.Field()
    genres = scrapy.Field()
    themes  = scrapy.Field()
    duration = scrapy.Field()
    rating = scrapy.Field()
    synopsis = scrapy.Field()
    cover_image = scrapy.Field()

    opening_themes = scrapy.Field()
    ending_themes = scrapy.Field()

    related_entries = scrapy.Field()

    social_links = scrapy.Field()
    resources_links = scrapy.Field()
    streaming_links = scrapy.Field()



    #Statistics informations
    score = scrapy.Field()
    ranked = scrapy.Field()
    popularity = scrapy.Field()
    members = scrapy.Field()
    favorites = scrapy.Field()

def remove_no_opening_themes(value):
    if value.startswith("No opening themes"):
        return ""
    return value

def remove_no_ending_themes(value):
    if value.startswith("No ending themes"):
        return ""
    return value


def remove_no_synopsis(value):
    if value.startswith("No synopsis information"):
        return ""
    return value

def clean_dict(value):
    value = value[0]
    replacement_dict = []

    for key, value in value.items():
        key_cleaned = re.sub('\\n|\\r', '', key)
        key_cleaned = re.sub("\s{2,}", " ", key_cleaned)
        key_cleaned = key_cleaned.replace(':', '')
        key_cleaned = key_cleaned.strip()

        if isinstance(value, list):
            list_cleaned = ""
            for list_value in value:
                list_value_cleaned = re.sub('\\n|\\r', '', list_value)
                list_value_cleaned = re.sub("\s{2,}", " ", list_value_cleaned)
                list_value_cleaned = list_value_cleaned.strip()
                list_cleaned += list_value_cleaned + ' ; '
            replacement_dict.append(key_cleaned + " - (" + list_cleaned + ")")
            continue
        else:
            value_cleaned = re.sub('\\n|\\r', '', value)
            value_cleaned = re.sub("\s{2,}", " ", value_cleaned)
            value_cleaned = value_cleaned.strip()
            replacement_dict.append(key_cleaned + ' - ('+value_cleaned+')')
            continue

    print("dict cleaned :", replacement_dict)
    return replacement_dict

class AnimeLoader(ItemLoader):
    default_output_processor = MapCompose(
                                          lambda x: x.strip(),
                                          lambda x:re.sub('\\n|\\r', '', x), 
                                          lambda x:re.sub("\s{2,}", " ", x), 
                                          lambda x:x.replace('"' ,"'"),
                                          lambda x: remove_no_ending_themes(x),
                                          lambda x: remove_no_synopsis(x),
                                          lambda x:remove_no_opening_themes(x),
                                          lambda x: None if re.sub(r'^$|^,$|add some|None\s*found.', '', x) == '' else x
                                          )

    airing_date_in = TakeFirst()
    broadcast_date_in = TakeFirst()
    duration_in = TakeFirst() 

    genres_in = Compose(set, list)
    social_links_in = Compose(set, list)
    resources_links_in = Compose(set, list)
    streaming_links_in = Compose(set, list)
    themes_in = Compose(set, list)
    demographic_in = Compose(set, list)
    
    episodes_number_in = TakeFirst()
    cover_image_in = TakeFirst()
    favorites_in = TakeFirst()
    members_in = TakeFirst()
    popularity_in = TakeFirst()
    premiered_date_in = TakeFirst()
    ranked_in = TakeFirst()
    rating_in = TakeFirst()
    source_in = TakeFirst()
    status_in = TakeFirst()
    score_in = TakeFirst()
    opening_themes_in = Join()

    ending_themes_in = Join()

    synopsis_in = Join()

    type_in = TakeFirst()

    related_entries_in = Compose(clean_dict, Join(' | '))


