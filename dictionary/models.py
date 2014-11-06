from django.db import models

# Create your models here.


class Word(models.Model):

    def __unicode__(self):
        return self.word

    word = models.CharField(max_length=40)


class Row(models.Model):

    def __unicode__(self):

        # would like to have all the words from the row displayed, but it's too sql-heavy
        return u'{0} ({1})'.format(self.name, self.author)

    name = models.CharField(max_length=40)  # could come from the dominant, I guess, needed for admin display
    author = models.CharField(max_length=40)
    sense = models.TextField()
    words = models.ManyToManyField(Word, through='Status')


class Status(models.Model):

    def __unicode__(self):
        return u'{0} ({1}), row {2}'.format(self.word.word, self.status, self.row.name)

    STATUS_CHOICES = (
        ('D', 'dominant'),
        ('S', 'synonym'),
        ('L', 'link')
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    word = models.ForeignKey(Word)
    row = models.ForeignKey(Row)

# todo (maybe) check there's only one dominant in each row