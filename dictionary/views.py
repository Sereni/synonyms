from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from models import Word, Row, SubRow, Synonym
from django.views.generic.base import View
# todo in all templates, change links from asdf.html to /fdsa


class Index(View):

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
            # todo process the rows in a representation function
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


            pks = [row.id for row in rows]
        return render_to_response('dictionary/../templates/main.html', {'pks': pks})


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