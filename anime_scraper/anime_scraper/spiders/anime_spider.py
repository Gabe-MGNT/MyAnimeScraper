import scrapy
from  ..items import AnimeLoader, Anime

class AnimeScraper(scrapy.Spider):
    name = "AnimeScraper"
    start_urls = ["https://myanimelist.net/anime.php"]
    search_letters = [".", "A", "B", "C", "D", "E", "F", "G", "H", "I","J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U","V", "W", "X", "Y", "Z"]

    def __init__(self, *args, **kwargs):
        super(AnimeScraper, self).__init__(*args, **kwargs)


    def parse(self, response):

        """
        yield scrapy.Request(
                    url="https://myanimelist.net/anime/52299/Ore_dake_Level_Up_na_Ken",
                    callback=self.parse_anime_page
                )
        """
        
        
        for letter in self.search_letters:
            url_with_character = f"https://myanimelist.net/anime.php?letter={letter}"
            
            yield scrapy.Request(
                url=url_with_character,
                callback=self.parse_letter_page
            )
        
        



    
    def parse_letter_page(self, response):

        max_page_number_str = response.xpath("//a[contains(@href, 'show')]/text()").getall()[-1]

        try:
            max_page_number_int = int(max_page_number_str)
        except ValueError:
            raise ValueError("Could not convert or find max_page_number_str to int on page: "+response.url)
        
        for page_number in range(0, max_page_number_int):
            url_with_page_number = f"{response.url}&show={str(page_number*50)}"

            yield scrapy.Request(
                url=url_with_page_number,
                callback=self.parse_page_with_animes_list,
            )

            
    def parse_page_with_animes_list(self, response):
        anime_page_links = response.xpath("//div[@class='title']/a[re:match(@href, 'https:\S+\/anime\/[0-9]+\/\S+')]/@href").getall()

        for index, anime_url in enumerate(anime_page_links):
            yield scrapy.Request(
                url=anime_url,
                callback=self.parse_anime_page,
            )


    def parse_anime_page(self, response):
        anime_loader = AnimeLoader(item = Anime(), response=response)

        anime_loader.add_value("id", response.url.split("/")[-2])


        # LEFT PANEL
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
        anime_loader.add_xpath("score", "//div/*[starts-with(text(),'Score:')]/following-sibling::*/text()")
        anime_loader.add_xpath("ranked", "//div/*[starts-with(text(),'Ranked:')]/following-sibling::text()")
        anime_loader.add_xpath("popularity", "//div/*[starts-with(text(),'Popularity:')]/following-sibling::text()")
        anime_loader.add_xpath("members", "//div/*[starts-with(text(),'Members:')]/following-sibling::text()")
        anime_loader.add_xpath("favorites", "//div/*[starts-with(text(),'Favorites:')]/following-sibling::text()")

        anime_loader.add_xpath("synopsis", "//div[h2[contains(.,'Synopsis')]]/following-sibling::p//text()")
        anime_loader.add_xpath("cover_image", "//a[contains(@href,'pics')]/img/@data-src")


        anime_loader.add_xpath("demographic", "//div/*[starts-with(text(),'Demographic:')]/following-sibling::*//text()")
        anime_loader.add_xpath("demographic", "//div/*[starts-with(text(),'Demographic:')]/following-sibling::text()")

        # ENDING PANEL
        endings = response.xpath("//div[h2[contains(.,'Ending Theme')]]/following-sibling::div/table//tr")
        for ending in range(1,len(endings)+1):
            #anime_loader.add_xpath("ending_themes", f"//div[h2[contains(.,'Ending Theme')]]/following-sibling::*//tr[{ending}]//span//text()")
            anime_loader.add_xpath("ending_themes", f"//div[h2[contains(.,'Ending Theme')]]/following-sibling::div/table//tr[{ending}]//text()")


        # OPENING PANEL
        openings = response.xpath("//div[h2[contains(.,'Opening Theme')]]/following-sibling::div/table//tr")
        for opening in range(1, len(openings)+1):
            #anime_loader.add_xpath("opening_themes", f"//div[h2[contains(.,'Ending Theme')]]/following-sibling::*//tr[{opening}]//span//text()")
            anime_loader.add_xpath("opening_themes", f"//div[h2[contains(.,'Opening Theme')]]/following-sibling::div/table//tr[{opening}]//text()")

        # RELATED ENTRIES
        relations_dict = {}
        entries_tile = response.xpath('//div[contains(@class, "related-entries")]/div')
        for entry_tile in entries_tile:
            relation = entry_tile.xpath('.//div[contains(@class, "relation")]/text()').get()
            link = entry_tile.xpath('.//div[contains(@class, "title")]/a/@href').get()
            if relation is None:
                continue
            relations_dict[relation] = link

        entry_table = response.xpath('//table[contains(@class, "entries-table")]/tr')
        for entry in entry_table:
            relation = entry.xpath('./td[1]/text()').get()
            link = entry.xpath('./td[2]//a/@href').getall()
            if relation is None:
                continue
            relations_dict[relation] = link

        anime_loader.add_value("related_entries", relations_dict)


        # SOCIAL LINKS
        social_links = response.xpath("//h2[contains(.,'Available At')]/following-sibling::div[1]//a/@href").getall() 
        for social_link in social_links:
            if len(social_link) >1:
                anime_loader.add_value("social_links", social_link)

        # RESOURCES LINKS
        resources_links = response.xpath("//h2[contains(.,'Resources')]/following-sibling::div[1]//a/@href").getall()
        for resource_link in resources_links:
            if len(resource_link) >1:
                anime_loader.add_value("resources_links", resource_link)

        # STREAMING LINKS
        streaming_links = response.xpath("//h2[contains(.,'Streaming Platforms')]/following-sibling::div[1]//a/@href").getall()
        for streaming_link in streaming_links:
                if 'javascript' in streaming_link:
                    continue
                if len(streaming_link) >1:
                    anime_loader.add_value("streaming_links", streaming_link)
                
            
        return anime_loader.load_item()
