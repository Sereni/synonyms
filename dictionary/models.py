from django.db import models

# Create your models here.


class Word(models.Model):
    word = models.CharField(max_length=40)


class Row(models.Model):
    author = models.CharField(max_length=40)
    sense = models.TextField()
    words = models.ManyToManyField(Word, through='Status')


class Status(models.Model):

    STATUS_CHOICES = (
        ('D', 'dominant'),
        ('S', 'synonym'),
        ('L', 'link')
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    word = models.ForeignKey(Word)
    row = models.ForeignKey(Row)

# todo row needs a name
# todo (maybe) check there's only one dominant in each row