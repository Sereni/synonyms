__author__ = 'Sereni'
from django.contrib import admin
from dictionary.models import Word, Row, Status


class WordAdmin(admin.ModelAdmin):
    list_display = 'word'


class RowAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')  # it'd be nice to have all words here, but that'd be sql-heavy. any ideas?


class StatusAdmin(admin.ModelAdmin):
    list_display = ('word', 'status', 'row.name')

admin.site.register(Word)
admin.site.register(Row)
admin.site.register(Status)

# todo readable names in admin
# todo display words in Row admin
# todo (maybe) display rows in Word admin