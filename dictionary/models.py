from django.db import models

# Create your models here.


class Word(models.Model):

    def __unicode__(self):
        return self.word

    word = models.CharField(max_length=200)  # there are some ridiculously long phrases for synonyms
    #lemma = models.CharField(max_length=40)


class Row(models.Model):

    def __unicode__(self):

        # would like to have all the words from the row displayed, but it's too sql-heavy
        return u'{0}'.format(self.dominant)

    dominant = models.ForeignKey(Word)  # should we make that a string or a foreign key to word?
    sense = models.TextField()
    example = models.TextField()
    phrase = models.TextField()


class SubRow(models.Model):

    groupid = models.CharField(max_length=2)  # can be an integer, a dash '-' or an empty string
    rowid = models.CharField(max_length=2)
    row = models.ForeignKey(Row)
    words = models.ManyToManyField(Word, through='Synonym')


class Synonym(models.Model):

    def __unicode__(self):
        return u'{0} ({1})'.format(self.word.word, self.subrow.row.dominant)  # ridiculously expensive

    word = models.ForeignKey(Word)
    author = models.CharField(max_length=200)  # authors that put this synonym into this subrow, string, separated
    mark = models.CharField(max_length=200)  # a mark (colloquial, etc) pertaining to this particular word in this row
    subrow = models.ForeignKey(SubRow)  # should be null for dominant

# todo (maybe) check there's only one dominant in each row