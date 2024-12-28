# MyAnimeScraper

MyAnimeScraper is a web scraper specifically designed for extracting data from the website MyAnimeList. I've finnaly managed to release this third version that is much more simple, but working.

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/7/7a/MyAnimeList_Logo.png">
</p>

This scraper use [Scrapy](https://scrapy.org/) as a foundation, to make easily extract data and be fast. MyAnimeList does ban bot doing too much request at a time, but doesn't bot, that's why the choice of Scrapy. In order to extract data without flooding the website, a download delay has been set to 7 (which is quite reasonable but you can modify it).


## How does it works ?
### Iterate through all letters
The anime search on MAL can be made by the beginning letter of the anime title, so the scraper iterate over the 27 (26 letters plus the non-letter) possibilites, and goes through every possible letter (here letter 'B').

![Anime with letter B](img/B-page.png)

Once a letter has been selected, it checks the maximum of subpages number (here 20), and scrap all the animes on all these pages by going on every link.

### Anime informations
The current version take all the informations on the anime landing page : it goes from the cover picture, to the statistical numbers (like rank, popularity, members), to details informations (title, studios, licensors, season).

<p align="center">
  <img src="img/steins_gate_page copy.png">
</p>
(Red square are the informations retrieved)



## How to use it ?
Scrapy spiders are ofently used by typing in the terminal, to make things easier there's a <code>main.py</code> that execute the scraper. 

In this file, you can choose the output file name.

```
python main.py
```


## Further parameters to modify
Other parameters can be modifies except from the output file name.

The scraper itself can be modified at <code>anime_scraper/anime_scraper/spiders/anime_spider.py</code> 

The parameters and settings from the spider can be found at <code>anime_scraper/anime_scraper/settings.py</code>
And in this specific file you can modify the number of concurrent request, and the delay between each request (base at 7 secondes to not overflood).

## Future Improvements
Incoming