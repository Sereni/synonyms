__author__ = 'Sereni'
"""
This is a script to extract dictionary data from the combinedDictionary.xml
and save it to the database.
"""

from xml.etree import ElementTree as ET
from dictionary.models import Word, Row, SubRow, Synonym



def find_words(xmlroot):
    words = set([])
    for chunk in root:

        # save the dominant
        words.add(chunk.attrib['dominant'])

        # find the row
        for item in chunk:
            if item.tag == 'syn_row':
                row = item
                break

        # save all synonyms from the row
        for synonym in row:

            # except for the 'redirect' rows
            if synonym.attrib['redirect']:
                continue

            words.add(synonym.text)
    return words


# tree = ET.parse('combinedDictionary.txt')
tree = ET.parse('minidict.xml')
root = tree.getroot()

# find words
words = find_words(root)

# save to db
for item in words:
    word = Word(word=item)
    word.save()

# todo extract one row. write down dominant, sense, examples, phrase
# look up dominant and write its pk
# fill the disconnected fields

# todo create corresponding subrows
# make a list of rowid, groupid pairs from synonym tags
# for each pair, create a subrow object connected to the row
# save subrow

# todo link words to subrows
# for each word in syn tag
#   look up its pk
#   from tag attribute, write author and mark
#   read groupid and rowid
#   find subrow by groupid and rowid, they are not saved yet, python objects!
#   create and save a Synonym instance

# PROFIT