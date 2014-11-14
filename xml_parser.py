# coding=utf-8
__author__ = 'Sereni'
"""
This is a script to extract dictionary data from the combinedDictionary.xml
and save it to the database.
"""

import sys, os

# note: the path is hardcoded on the next line. change accordingly.
sys.path.append('/Users/Sereni/PycharmProjects/synonyms/synonyms')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


from xml.etree import ElementTree as ET
from dictionary.models import Word, Row, SubRow, Synonym


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

# todo handle empty fields
# phrase may be [] for empty
# example may be None for empty
# all of them may just be empty
# todo parse example for author
def extract_row(rowxml):
    for child in rowxml:
        if child.tag == 'sense':
            sense = child.text
        elif child.tag == 'examples':
            example = child.text
        elif child.tag == 'phrase_row':
            phrase = child.text
    dominant = Word.objects.filter(word=rowxml.attrib['dominant'])
    row = Row(dominant=dominant,
              sense=sense,
              example=example,
              phrase=phrase
              )
    return row.save()


# all sorts of poorly formatted data in the dictionary on this part
# will have to invent crutches on display
# todo handle empty ids
def get_subrow_ids(rowxml):
    """
    Makes a list of tuples (rowid, groupid) found in the row xml
    """
    ids = set([])
    for synrow in rowxml:
        ids.add(synrow.attrib['rowid'], synrow.attrib['groupid'])
    return ids


def create_subrows(ids, row):
    """
    Creates subrow instances from rowid, groupid; links them to synonym
    row adn writes to db.
    """
    for (rowid, groupid) in ids:
        subrow = SubRow(
            rowid=rowid,
            groupid=groupid,
            row=row
        )
        subrow.save()

# todo add checks for empty attribs. add placeholders
def create_link(xml):
    subrow = SubRow.objects.get(groupid=xml.attrib['groupid'],
                                rowid=xml.attrib['rowid'],
                                row=new_row.pk)
    word = Word.objects.get(word=syn_xml.text)
    author = xml.attrib['dict']  # writing it raw, will parse/replace in views
    if xml.attrib['mark']:
        mark = xml.attrib['mark']
    else:
        mark = '#'  # placeholder for anything that can't be empty
    synonym = Synonym(
        word=word,
        subrow=subrow,
        mark=mark,
        author=author
    )
    synonym.save()

# tree = ET.parse('combinedDictionary.txt')
tree = ET.parse('minidict.xml')
root = tree.getroot()

# find words
words = find_words(root)

# save to db
for item in words:
    word = Word(word=item)
    word.save()

# create rows
for row in root:
    new_row = extract_row(row)

    # create subrows
    subrow_ids = get_subrow_ids(row)
    create_subrows(subrow_ids, new_row.pk)

    # link words to subrows
    synrow = row.find('syn_row')
    for syn_xml in synrow:
        create_link(syn_xml)
        # look up the subrow
        subrow = SubRow.objects.get(groupid=syn_xml.attrib['groupid'],
                                    rowid=syn_xml.attrib['rowid'],
                                    row=new_row.pk)
        word = Word.objects.get(word=syn_xml.text)


# PROFIT