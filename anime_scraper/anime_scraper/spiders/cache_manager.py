import pickle

class CacheManager:
    def __init__(self, cache_file='crawl_cache.pkl'):
        self.cache_file = cache_file
        self.crawled_urls = set()

    def load_cache(self):
        try:
            with open(self.cache_file, 'rb') as f:
                self.crawled_urls = pickle.load(f)
        except FileNotFoundError:
            # Le fichier n'existe pas encore, c'est normal au début
            pass

    def save_cache(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.crawled_urls, f)

    def is_url_crawled(self, url):
        return url in self.crawled_urls

    def mark_url_as_crawled(self, url):
        self.crawled_urls.add(url)
        self.save_cache()
