# coding=utf-8
__author__ = 'Sereni'
"""
This is a script to extract dictionary data from the combinedDictionary.xml
and save it to the database.
"""

import sys, os
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

# note: the path is hardcoded on the next line. change accordingly.
sys.path.append('/Users/Sereni/PycharmProjects/synonyms/synonyms')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


from xml.etree import ElementTree as ET
from dictionary.models import Word, Row, SubRow, Synonym


def lemmatize(text):
    lemmas = ''
    for word in text.split(' '):
        lemmas += morph.parse(word.strip(u'(<{«)>}»-‒–—―.,:?!;;%‰‱··]$^[]'))[0].normal_form + ' '
    # this returns the most probable lemma
    # uncomment next line to get all possible lemmas for each word:
    # lemmas += ' '.join(ana.normal_form for ana in morph.parse(word.strip())) + ' '

    return lemmas.strip(' ')


def find_words(xmlroot):
    words = set([])
    for chunk in xmlroot:

        # save the dominant
        words.add(chunk.attrib['dominant'])

        # find the row
        for item in chunk:
            if item.tag == 'syn_row':
                row = item
                break

        # save all synonyms from the row
        for synonym in row:

            # except for the 'redirect' rows. code 'em like a n00b
            # note: I have removed both 'перенаправлено' and
            # 'подробнее', search option 'ряды' should compensate
            try:
                synonym.attrib['redirect']
            except KeyError:
                words.add(synonym.text)
    return words


def check_for_empty(s):
    if s == '[]' or s == 'None' or not s:
        return '#'
    return s


def extract_row(rowxml):
    for child in rowxml:
        if child.tag == 'sense':
            sense = pretty_authors(check_for_empty(child.text)).replace('[', '').replace(':', '').\
                replace(']', '').strip(' ')
        elif child.tag == 'examples':
            example = check_for_empty(child.text)
        elif child.tag == 'phrase_row':
            phrase = check_for_empty(child.text)
    if len(rowxml.attrib['dominant']) > 60:
        return None
    dominant = Word.objects.get(word=rowxml.attrib['dominant'])
    row, created = Row.objects.get_or_create(dominant=dominant,
                                             sense=sense,
                                             lemmatized_sense=lemmatize(sense),
                                             example=example,
                                             phrase=phrase,
                                             lemmatized_phrase=lemmatize(phrase)
                                             )
    return row


def pretty_id(i):
    """
    This handles the cases of row and group ids looking like '1abr'
    Also replaces empty ids '' with '#'
    """
    if i:
        try:
            i / 2
        except TypeError:
            if i == '-':
                pass
            else:
                return i[0]
    else:
        return '#'
    return i


# all sorts of poorly formatted data in the dictionary on this part
# will have to invent crutches on display
def get_subrow_ids(rowxml):
    """
    Makes a list of tuples (rowid, groupid) found in the row xml
    """
    ids = set([])
    synrow = rowxml.find('syn_row')
    for s in synrow:
        row_id = pretty_id(s.attrib['rowid'])
        group_id = pretty_id(s.attrib['groupid'])
        ids.add((row_id, group_id))

    return ids


def create_subrows(ids, row):
    """
    Creates subrow instances from rowid, groupid; links them to synonym
    row adn writes to db.
    """
    for (rowid, groupid) in ids:
        SubRow.objects.get_or_create(
            rowid=rowid,
            groupid=groupid,
            row=row
        )


def pretty_authors(s):
    """
    Replaces dictionary file names with authors' names
    """
    replacements = {
            u'babenko.txt': u'Бабенко',
            u'noss.txt': u'НОСС',
            u'aleks.txt': u'Александрова',
            u'abramov.txt': u'Абрамов',
            u'evgen.txt': u'Евгеньева'
        }
    for key, value in replacements.items():
            s = s.replace(key, value)
    return s

def create_link(xml):
    subrow = SubRow.objects.get(groupid=pretty_id(xml.attrib['groupid']),
                                rowid=pretty_id(xml.attrib['rowid']),
                                row=new_row)
    if len(xml.text) > 60:
        return
    word = Word.objects.get(word=xml.text)
    author = pretty_authors(xml.attrib['dict'])
    if xml.attrib['mark']:
        mark = xml.attrib['mark']
    else:
        mark = '#'  # placeholder for anything that can't be empty
    Synonym.objects.get_or_create(
        word=word,
        subrow=subrow,
        mark=mark,
        author=author
    )

# tree = ET.parse('combinedDictionary.txt')
tree = ET.parse('dict_full.xml')
root = tree.getroot()

# find words
words = find_words(root)

# save to db
for item in words:

    # all sorts of crap in xml, will have to handle manually
    if len(item) > 60:
        continue
    else:
        Word.objects.get_or_create(word=item)

# create rows
for row in root:
    new_row = extract_row(row)
    if not new_row:
        continue  # means this is one of the rows with overly long dominants, add manually later on

    # create subrows
    subrow_ids = get_subrow_ids(row)
    create_subrows(subrow_ids, new_row)

    # link words to subrows
    synrow = row.find('syn_row')
    for syn_xml in synrow:
        try:
            syn_xml.attrib['redirect']  # now, I'm not sure it's correct to skip those... # todo
            continue
        except:
            create_link(syn_xml)