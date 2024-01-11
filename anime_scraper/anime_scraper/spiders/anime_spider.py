import scrapy
from  ..items import AnimeLoader, Anime
from .cache_manager import CacheManager

class AnimeScraper(scrapy.Spider):
    name = "AnimeScraper"
    start_urls = ["https://myanimelist.net/anime.php"]
    search_characters = [".", "A", "B", "C", "D", "E", "F", "G", "H", "I","J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U","V", "W", "X", "Y", "Z"]

    def __init__(self, *args, **kwargs):
        super(AnimeScraper, self).__init__(*args, **kwargs)
        self.cache_manager = CacheManager()
        self.cache_manager.load_cache()

    def parse(self, response):
        for character in self.search_characters:
            url_with_character = "https://myanimelist.net/anime.php?letter="+character
            
            yield scrapy.Request(
                url=url_with_character,
                callback=self.parse_character_page
            )


            """
            if not self.cache_manager.is_url_crawled("https://myanimelist.net/anime/52299/Ore_dake_Level_Up_na_Ken"):
                yield scrapy.Request(
                    url="https://myanimelist.net/anime/52299/Ore_dake_Level_Up_na_Ken",
                    callback=self.parse_anime_page
                )
            else:
                self.log(f"URL https://myanimelist.net/anime/52299/Ore_dake_Level_Up_na_Ken already crawled, skipping")
            """
    def parse_character_page(self, response):

        max_page_number_str = response.xpath("//a[contains(@href, 'show')]/text()").getall()[-1]
        try:
            max_page_number_int = int(max_page_number_str)
        except ValueError:
            raise ValueError("Could not convert max_page_number_str to int on page: "+response.url)
        
        for page_number in range(0, max_page_number_int):
            url_with_page_number = response.url+"&show="+str(page_number*50)

            yield scrapy.Request(
                url=url_with_page_number,
                callback=self.parse_page_with_animes
            )


            
    def parse_page_with_animes(self, response):
        anime_page_urls = response.xpath("//div[@class='title']/a[re:match(@href, 'https:\S+\/anime\/[0-9]+\/\S+')]/@href").getall()
        for anime_url in anime_page_urls:

            if not self.cache_manager.is_url_crawled(response.url):
                yield scrapy.Request(
                    url=anime_url,
                    callback=self.parse_anime_page
                )
            else:
                self.log(f"URL {response.url} already crawled, skipping")



    def parse_anime_page(self, response):
        anime_loader = AnimeLoader(item = Anime(), response=response)

        anime_loader.add_value("id", response.url.split("/")[-2])
        anime_loader.add_css("original_title", 'h1 ::text')
        anime_loader.add_xpath("japanese_title", "//*[starts-with(text(),'Japanese:')]/following-sibling::text()")
        anime_loader.add_xpath("english_title", "//*[starts-with(text(),'English:')]/following-sibling::text()")
        anime_loader.add_xpath("synonyms", "//*[starts-with(text(),'Synonyms:')]/following-sibling::text()")

        anime_loader.add_xpath("type", "//*[starts-with(text(),'Type:')]/following-sibling::*/text()")
        anime_loader.add_xpath("episodes_number", "//*[starts-with(text(),'Episodes:')]/following-sibling::text()")
        anime_loader.add_xpath("status", "//div/*[starts-with(text(),'Status:')]/following-sibling::text()")
        anime_loader.add_xpath("airing_date", "//div/*[starts-with(text(),'Aired:')]/following-sibling::text()")
        anime_loader.add_xpath("premiered_date", "//div/*[starts-with(text(),'Premiered:')]/following-sibling::*/text()")
        anime_loader.add_xpath("broadcast_date", "//div/*[starts-with(text(),'Broadcast:')]/following-sibling::text()")
        
        anime_loader.add_xpath("producers", "//div/*[starts-with(text(),'Producers:')]/following-sibling::*//text()")
        anime_loader.add_xpath("producers", "//div/*[starts-with(text(),'Producers:')]/following-sibling::text()")

        anime_loader.add_xpath("licensors", "//div/*[starts-with(text(),'Licensors:')]/following-sibling::*//text()")
        anime_loader.add_xpath("licensors", "//div/*[starts-with(text(),'Licensors:')]/following-sibling::text()")

        anime_loader.add_xpath("studios", "//div/*[starts-with(text(),'Studios:')]/following-sibling::*//text()")
        anime_loader.add_xpath("studios", "//div/*[starts-with(text(),'Studios:')]/following-sibling::text()")

        anime_loader.add_xpath("source", "//div/*[starts-with(text(),'Source:')]/following-sibling::text()")

        anime_loader.add_xpath("genres", "//div/*[starts-with(text(),'Genres:')]/following-sibling::*//text()")
        anime_loader.add_xpath("genres", "//div/*[starts-with(text(),'Genres:')]/following-sibling::text()")

        anime_loader.add_xpath("themes", "//div/*[starts-with(text(),'Theme:')]/following-sibling::*//text()")
        anime_loader.add_xpath("themes", "//div/*[starts-with(text(),'Theme:')]/following-sibling::text()")

        anime_loader.add_xpath("duration", "//div/*[starts-with(text(),'Duration:')]/following-sibling::text()")
        anime_loader.add_xpath("rating", "//div/*[starts-with(text(),'Rating:')]/following-sibling::text()")
        anime_loader.add_xpath("synopsis", "//div[h2[contains(.,'Synopsis')]]/following-sibling::p//text()")
        anime_loader.add_xpath("score", "//div/*[starts-with(text(),'Score:')]/following-sibling::*/text()")
        anime_loader.add_xpath("ranked", "//div/*[starts-with(text(),'Ranked:')]/following-sibling::text()")
        anime_loader.add_xpath("popularity", "//div/*[starts-with(text(),'Popularity:')]/following-sibling::text()")
        anime_loader.add_xpath("members", "//div/*[starts-with(text(),'Members:')]/following-sibling::text()")
        anime_loader.add_xpath("favorites", "//div/*[starts-with(text(),'Favorites:')]/following-sibling::text()")
        
        endings = response.xpath("//div[h2[contains(.,'Ending Theme')]]/following-sibling::div/table//tr")
        for ending in range(1,len(endings)+1):
            #anime_loader.add_xpath("ending_themes", f"//div[h2[contains(.,'Ending Theme')]]/following-sibling::*//tr[{ending}]//span//text()")
            anime_loader.add_xpath("ending_themes", f"//div[h2[contains(.,'Ending Theme')]]/following-sibling::div/table//tr[{ending}]//text()")


        # OPENING THEME MAL RECUP2R2
        openings = response.xpath("//div[h2[contains(.,'Opening Theme')]]/following-sibling::div/table//tr")
        for opening in range(1, len(openings)+1):
            #anime_loader.add_xpath("opening_themes", f"//div[h2[contains(.,'Ending Theme')]]/following-sibling::*//tr[{opening}]//span//text()")
            anime_loader.add_xpath("opening_themes", f"//div[h2[contains(.,'Opening Theme')]]/following-sibling::div/table//tr[{opening}]//text()")


        yield anime_loader.load_item()
        self.cache_manager.mark_url_as_crawled(response.url)