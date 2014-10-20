__author__ = 'Sereni'
from django.contrib import admin
from dictionary.models import Word, Row, Status

admin.site.register(Word)
admin.site.register(Row)
admin.site.register(Status)

# todo readable names in admin
# todo display words in Row admin
# todo (maybe) display rows in Word admin