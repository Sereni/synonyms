__author__ = 'Sereni'
from django.contrib import admin
from dictionary.models import Word, Row, Synonym, SubRow


class WordAdmin(admin.ModelAdmin):
    list_display = 'word'


class RowAdmin(admin.ModelAdmin):
    list_display = ('dominant',)  # it'd be nice to have all words here, but that'd be sql-heavy. any ideas?


class StatusAdmin(admin.ModelAdmin):
    list_display = ('word', 'status', 'subrow.row.dominant')


class SubRowAdmin(admin.ModelAdmin):
    list_display = ('rowid', 'groupid', 'row.dominant')

admin.site.register(Word)
admin.site.register(Row)
admin.site.register(Synonym)
admin.site.register(SubRow)


# todo display words in Row admin
# todo (maybe) display rows in Word admin