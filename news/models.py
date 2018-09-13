from django.db import models

class News(models.Model):
    label = models.IntegerField()
    title = models.CharField(max_length=100)
    time = models.CharField(max_length=25)
    source = models.CharField(max_length=15)
    text = models.TextField()

    def __str__(self):
        return str(self.label)

# Create your models here.
