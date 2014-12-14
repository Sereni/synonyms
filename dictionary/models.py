from django.db import models

# Create your models here.


class Word(models.Model):

    def __unicode__(self):
        return self.word

    word = models.CharField(max_length=200, db_index=True)  # there are some ridiculously long phrases for synonyms


class Row(models.Model):

    def __unicode__(self):

        # should you ever wonder why subrows take 30 seconds to load in admin, this is the line.
        return u'{0}'.format(self.dominant)

    dominant = models.ForeignKey(Word)
    sense = models.TextField(db_index=True)
    lemmatized_sense = models.TextField(db_index=True)  # lemmatized sense string
    example = models.TextField()
    phrase = models.TextField()
    lemmatized_phrase = models.TextField()  # lemmatized phrasesyn string


class SubRow(models.Model):

    groupid = models.CharField(max_length=2)
    rowid = models.CharField(max_length=2)
    row = models.ForeignKey(Row)
    words = models.ManyToManyField(Word, through='Synonym')


class Synonym(models.Model):

    def __unicode__(self):
        return u'{0} ({1})'.format(self.word.word, self.subrow.row.dominant)

    word = models.ForeignKey(Word)
    author = models.CharField(max_length=200)  # authors that put this synonym into this subrow, string, separated
    mark = models.CharField(max_length=200)  # a mark (colloquial, etc) pertaining to this particular word in this row
    subrow = models.ForeignKey(SubRow)  # should be null for dominant
