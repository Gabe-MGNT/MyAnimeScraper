from scrapy.crawler import CrawlerProcess
from anime_scraper.anime_scraper.spiders.anime_spider import MyAnimeSpider
from scrapy.utils.project import get_project_settings

def main():

    settings = get_project_settings()

    settings['FEED_URI'] = 'test9.csv'
    process = CrawlerProcess(settings=settings)
    process.crawl(MyAnimeSpider)
    process.start()  # the script will block here until the crawling is finished

if __name__ == "__main__":
    main()