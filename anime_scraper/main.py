from scrapy.crawler import CrawlerProcess
from anime_scraper.spiders.anime_spider import AnimeScraper
from scrapy.utils.project import get_project_settings


def main():
    settings = get_project_settings()
    settings['FEED_URI'] = 'test2.csv'
    settings['FEED_FORMAT'] = 'csv'
    process = CrawlerProcess(settings=settings)
    process.crawl(AnimeScraper)
    process.start()

if __name__ == "__main__":
    main()