import os
import django
from django.db import connection
from django.db.models import Q
from django.db.models.aggregates import Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author
# Import your models here

def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ""

    query= Q()
    if search_name:
        query &=Q(full_name__icontains= search_name)
    if search_email:
        query &= Q(email__icontains = search_email)
    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors.exists():
        return ""

    return '\n'.join(
        f"Author: {a.full_name}, email: {a.email}, status: {'Banned' if a.is_banned else 'Not Banned'}"
        for a in authors
    )




def get_top_publisher():
    top_publisher = (Author.objects
                     .get_authors_by_article_count()
                     .filter(number_of_articles__gt=0)
                     .first()
                     )

    if not top_publisher:
        return ""

    return f"Top Author: {top_publisher.full_name} with {top_publisher.number_of_articles} published articles."



def get_top_reviewer():
    top_reviewer = (Author.objects
                    .annotate(num_of_reviews = Count('reviews'))
                    .filter(num_of_reviews__gt= 0)
                    .order_by('-num_of_reviews', 'email')
                    .first()
                    )

    if not top_reviewer:
        return ""

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.num_of_reviews} published reviews."












