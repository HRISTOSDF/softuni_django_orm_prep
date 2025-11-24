from django.db import models
from django.db.models.aggregates import Count


class AuthorQuerySet(models.QuerySet):
    def get_authors_by_article_count(self):
        return self.annotate(number_of_articles= Count('articles')).order_by('-number_of_articles', 'email')