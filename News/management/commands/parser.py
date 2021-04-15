from django.core.management.base import BaseCommand
from django.utils import timezone
from newspaper import Article as NewsArticle

from News.management.commands import bot
from News.news_sites import *

RSS_Links = [
    'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    'http://feeds.foxnews.com/foxnews/world',
    'https://www.buzzfeed.com/world.xml',
    'https://www.aljazeera.com/xml/rss/all.xml',
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        reuters = Reuters('https://www.reuters.com/world')

        rss_news = RSSNews(RSS_Links)

        if reuters.urls:
            for url in reuters.urls:
                article = NewsArticle(url)
                article.download()
                article.parse()

                a = Article(title=article.title,
                            short_text=article.meta_description,
                            content=article.text,
                            date=timezone.now(),
                            author=article.authors,
                            source_link=url,
                            img=article.top_img)
                a.save()
                bot.send_message(a)

        if rss_news.urls:
            for url, date in rss_news.urls.items():
                article = NewsArticle(url)
                article.download()
                article.parse()

                a = Article(title=article.title,
                            short_text=article.meta_description,
                            content=article.text,
                            date=date,
                            author=article.authors,
                            source_link=url,
                            img=article.top_img)
                a.save()
                bot.send_message(a)

        self.stdout.write(self.style.SUCCESS('Success'))
