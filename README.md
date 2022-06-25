# python-ly-helpers
Utilities to help keep the python-ly words.py file up to date

## compare-lilypond-to-words.py
It's easy for python-ly/ly/words.py to get out of sync with the online documentation.
This script provides an easy way to compare words.py to the LilyPond online index. It
looks for entries online that start with a backslash (\) then checks words.py to see
if they are present there.  If not, the online term and a little context is printed.

## search-lilypond.py
When updating python-ly/ly/words.py with new commands, it's sometimes helpful to know the
earliest version it is found on, or to get some more context of the word.  This script searches
for a "raw" word (that is, unadorned) or with a backslash (\) prepended and a word boundary
at the end.  The changes, music functions, commands, and full index are searched from online
documents.  The different versions that a checked ar in the "versions" tuple.
