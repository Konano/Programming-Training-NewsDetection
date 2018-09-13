from django.db import models

class Dict(models.Model):
    news = models.IntegerField()
    word = models.CharField(max_length=10)
    times = models.IntegerField()

    def __str__(self):
        return str(self.times)

# Create your models here.
