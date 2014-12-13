# coding=utf-8
from django.shortcuts import render_to_response, redirect
from models import Word, Row, SubRow, Synonym
from django.views.generic.base import View
# todo in all templates, change links from asdf.html to /fdsa
# todo links to staticfiles in templates, as in main
# todo wtf is with the design, looks like crap, is it some static I'm missing or are we wasted for good?
# todo quit swearing in todos

class Index(View):

    def represent(self, rows):  # brace yourselves
        """
        Gets a list of Rows
        Returns a ridiculous structure that eats up templates' brains
        """
        d_rows = []
        for row in rows:

            # got all subrows of a row
            subrows = row.subrow_set.all()

            # constructing more convenient "display subrows"
            d_subrows = []
            for subrow in subrows:

                # got all the words in one subrow, along with their authors and marks
                words = [(synonym.author, synonym.mark, synonym.word.word) for synonym in subrow.synonym_set.all()]

                # wrote down a ('1.1', words) subrow
                d_subrow = ('.'.join([subrow.rowid, subrow.groupid]), words)
                d_subrows.append(d_subrow)
            d_rows.append((row, d_subrows))  # I'm passing a row and will call its attributes in template
        return d_rows

# todo убрать баяны [: [: [babenko.txt: Проявляющий заботу, внимание по отношению к кому , чему либо]][babenko.txt: Исполненный внимательного, беспокойного отношения к кому , чему либо и проявляющий подобное отношение в поступках, поведении]]

    def getWords(self, words):
        """
        Take a list of Word objects
        """


    def clean(self, query):
        # todo implement cleaning
        return query.lower().encode('utf-8')

    def get(self, request):
        return render_to_response('dictionary/../templates/main.html')

    def post(self, request):
        if 'simple' in request.POST.keys():
            kw = self.clean(request.POST['simple'])
            rows = Row.objects.filter(dominant__word=kw)

            # imitating activity
            pks = [row.id for row in rows]
            return render_to_response('dictionary/../templates/main.html', {'pks': pks})

        elif 'keywords' in request.POST.keys():
            query = self.clean(request.POST['keywords'])

            rows = []

            if 'dominant' in request.POST.keys():
                results = Row.objects.filter(dominant__word=query)
                results = [row for row in results if row not in rows]
                rows += results

            if 'row' in request.POST.keys():
                subrows = SubRow.objects.filter(words__word=query)
                for subrow in subrows:
                    row = subrow.row
                    if row not in rows:
                        rows.append(row)

            if 'definition' in request.POST.keys():

                # fixme this will return partial word matches; update to regex if unwanted
                results = Row.objects.filter(sense__contains=query)
                results = [row for row in results if row not in rows]
                rows += results

            if 'phrase' in request.POST.keys():
                results = Row.objects.filter(phrase__contains=query)
                results = [row for row in results if row not in rows]
                rows += results


            # pks = [row.id for row in rows]
            data = self.represent(rows)
        return render_to_response('dictionary/../templates/main.html', {'data': data})


def manual(request):
    """
    Returns a static how-to-use page
    """
    return render_to_response('dictionary/../templates/instruction.html')


def about(request):
    """
    Returns a static about page
    """
    return render_to_response('dictionary/../templates/about.html')


def bibliography(request):
    """
    Returns a static bibliography page
    """
    return render_to_response('dictionary/../templates/dictionaries.html')


# note: in current implementation, the difference between exact query and extended query over dominants
# is that extended query allows substring matching
# todo do we want to recreate this ^ behavior?


# todo extended search should have an explicit substring checkbox somewhere in the template