from django.db import models

class News(models.Model):
    label = models.IntegerField()
    def __str__(self):
        return str(self.label)

class Word(models.Model):
    name = models.CharField(max_length=10)
    news = models.ManyToManyField(News, through='Include')
    def __str__(self):
        return self.name

class Include(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)