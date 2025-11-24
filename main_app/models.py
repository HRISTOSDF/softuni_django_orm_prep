from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.mixins import PublishedOnMixin


# Create your models here.
class Author(models.Model):
    full_name = models.CharField(
        max_length= 3,
        validators= [MinLengthValidator(3)]
    )
    email = models.EmailField(
        unique= True
    )
    is_banned = models.BooleanField(
        default= False
    )
    birth_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2005)
        ]
    )
    website = models.URLField(
        blank= True,
        null= True
    )

class Article(PublishedOnMixin):
    title=  models.CharField(

    )