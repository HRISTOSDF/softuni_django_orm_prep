import os
import django
from django.db import connection


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q
from django.db.models.aggregates import Count, Avg

from main_app.models import Author, Article, Review


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


def get_latest_article():
    latest_article = (Article.objects
                      .annotate(number_of_reviews = Count('reviews'), avg_rating = Avg('reviews__rating'))
                      .filter(number_of_reviews__gt= 0)
                      .latest('published_on')
                      )

    if not latest_article:
        return ""

    authors = ', '.join([a.full_name for a in latest_article.authors.all().order_by('full_name')])

    return (f"The latest article is: {latest_article.title}. "
            f"Authors: {authors}. Reviewed: {latest_article.number_of_reviews} times."
            f" Average Rating: {latest_article.avg_rating:.2f}.")



def get_top_rated_article():
    top_article= (Article.objects
                  .annotate(avg_rating= Avg('reviews__rating'),num_reviews= Count('reviews'))
                  .filter(num_reviews__gt = 0)
                  .order_by('-avg_rating', 'title')
                  .first()
                  )

    if not top_article:
        return ""

    return (f"The top-rated article is: {top_article.title},"
            f" with an average rating of {top_article.avg_rating:.2f}, reviewed {top_article.num_reviews} times.")


def ban_author(email=None):
    if email is None:
        return "No authors banned."
    searched_author = Author.objects.annotate(num_reviews= Count('reviews')).filter(email__exact= email).first()

    if not searched_author:
        return "No authors banned."


    Review.objects.filter(author=searched_author.id).delete()

    Author.objects.filter(id= searched_author.id).update(is_banned= True)


    return f"{searched_author.full_name} is banned! {searched_author.num_reviews} reviews deleted."




