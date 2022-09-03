# coding=utf-8

from django.db import models


class Book(models.Model):
    name = models.CharField(u'Название', max_length=64)
    author = models.CharField(u'Автор', max_length=64)
    pub_date = models.DateField(u'Дата публикации')
    pub_date_str = models.CharField(max_length=10)
    image = models.URLField()

    def __str__(self):
        return self.name + " " + self.author
