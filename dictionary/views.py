# coding=utf-8
from django.shortcuts import render_to_response, redirect
from models import Word, Row, SubRow, Synonym
from django.views.generic.base import View
import re

class Index(View):

    def represent(self, rows, authors):  # brace yourselves
        """
        Gets a list of Rows
        Returns a ridiculous structure that eats up templates' brains
        """
        regSense = re.compile(u'(Бабенко|НОСС|Абрамов|Александрова|Евгеньева)')

        d_rows = []
        for row in rows:
            row.sense = regSense.sub(u'</br>\\1', row.sense)
            # got all subrows of a row
            subrows = row.subrow_set.all()

            # constructing more convenient "display subrows"
            d_subrows = []
            for subrow in subrows:

                # got all the words in one subrow, along with their authors and marks
                words = [(self.process_author(synonym.author), synonym.mark, synonym.word.word) for synonym in
                         subrow.synonym_set.all() if self.filter_author(synonym.author, authors)]

                # wrote down a ('1.1', words) subrow
                d_subrow = (self.process_ids(subrow.rowid, subrow.groupid), words)
                if d_subrow[0] and d_subrow[1]:
                    d_subrows.append(d_subrow)
            if d_subrows:
                d_rows.append((row, sorted(d_subrows)))  # I'm passing a row and will call its attributes in template
        return d_rows

    def filter_author(self, s, a):

        for author in a:
            if author in s:
                return True


    def process_ids(self, rowid, groupid):
        if rowid == '#' or groupid == '#':
            return
        if rowid == '-' or groupid == '-':
            return u'Без распределения по группам: '
        if rowid == '0':
            rowid = '1'
        groupid = '.' + groupid
        if groupid == '.0':
            groupid = ''
        return rowid + groupid

    def process_author(self, s):
        return ', '.join(s.split('|')), len(s.split('|'))


    def clean(self, query):
        # todo implement cleaning
        return query.lower().encode('utf-8')

    def get_authors(self, r):
        a = set([
            u'Бабенко',
            u'НОСС',
            u'Абрамов',
            u'Александрова',
            u'Евгеньева'
        ])

        return a.intersection(set(r))

    def get(self, request):
        return render_to_response('dictionary/../templates/main.html', {'data': ''})

    def post(self, request):
        if 'simple' in request.POST.keys():

            # simple doesn't accept any authors, we assume all at once. make it less hardcoded someday...
            auth_def = set([
            u'Бабенко',
            u'НОСС',
            u'Абрамов',
            u'Александрова',
            u'Евгеньева'
            ])
            kw = self.clean(request.POST['simple'])
            rows = Row.objects.filter(dominant__word=kw)

            data = self.represent(rows, auth_def)
            return render_to_response('dictionary/../templates/main.html', {'data': data})

        elif 'keywords' in request.POST.keys():
            query = self.clean(request.POST['keywords'])

            rows = []
            pattern = '(^|[:;()!?., ]){0}([:;()!?., ]|$)'.format(query)

            if 'dominant' in request.POST.keys():
                results = Row.objects.filter(dominant__word__regex=pattern)
                results = [row for row in results if row not in rows]
                rows += results

            if 'row' in request.POST.keys():
                subrows = SubRow.objects.filter(words__word__regex=pattern)
                for subrow in subrows:
                    row = subrow.row
                    if row not in rows:
                        rows.append(row)

            if 'definition' in request.POST.keys():

                results = Row.objects.filter(sense__regex=pattern) | Row.objects.filter(lemmatized_sense__regex=pattern)
                results = [row for row in results if row not in rows]
                rows += results
                print results

            if 'phrase' in request.POST.keys():
                results = Row.objects.filter(phrase__regex=pattern) | Row.objects.filter(lemmatized_phrase__regex=pattern)
                results = [row for row in results if row not in rows]
                rows += results

            authors = self.get_authors(request.POST.keys())
            data = self.represent(rows, authors)
        return render_to_response('dictionary/../templates/main.html', {'data': data, 'msg': True})


class Manual(Index):

    def get(self, request):
        return render_to_response('dictionary/../templates/instruction.html')


class About(Index):

    def get(self, request):
        return render_to_response('dictionary/../templates/about.html')


class Bibliography(Index):

    def get(self, request):
        return render_to_response('dictionary/../templates/dictionaries.html')