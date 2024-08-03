from django.core.cache import cache

from blog.models import Article
from config.settings import CACHE_ENABLED


def get_articles_from_cache():
    """
    Получение списка статей блога из кэша или БД.
    """
    if not CACHE_ENABLED:
        return Article.objects.all()
    else:
        key = 'categories_list'
        articles = cache.get(key)
        if articles is not None:
            return articles
        else:
            articles = Article.objects.all()
            cache.set(key, articles)
            return articles
