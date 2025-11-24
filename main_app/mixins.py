from django.db import models

class PublishedOnMixin(models.Model):
    published_on = models.DateTimeField(
        auto_now_add= True,
        editable= False
    )

    class Meta:
        abstract = True