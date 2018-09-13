from django.db import models

class News(models.Model):
    title = models.CharField(max_length=100)
    time = models.CharField(max_length=25)
    source = models.CharField(max_length=15)
    text = models.TextField()

    def __unicode__(self):
        return self.title

# Create your models here.
