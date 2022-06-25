# This program is protected by the Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
# (https://creativecommons.org/licenses/by-sa/4.0/)

import re
import argparse

from utils import get_text_from_html


class CompareLilyPondToWords:
    """
    It's easy for python-ly/ly/words.py to get out of sync with the online documentation.
    This class provides an easy way to compare words.py to the LilyPond online index. It
    looks for entries online that start with a backslash (\\\\) then checks words.py to see
    if they are present there.  If not, the online term and a little context is printed.
    """

    # Change this to the current LilyPond index or enter at the command line
    lilypond_index_url = "https://lilypond.org/doc/v2.23/Documentation/notation/lilypond-index"
    # Change this to the path to your python-ly/ly/words.py or enter at the command line
    python_ly_words_path = "/home/user_name/git-repos/python-ly/ly/words.py"
    # Find a quoted word in python-ly/ly/words.py
    find_quoted_word = r"\s*'([A-Za-z][-A-Za-z\d]*?)',"

    def get_args(self) -> None:
        """Get flags from command line and set documentation URL and words.py path accordingly"""
        parser = argparse.ArgumentParser(description='Compare python-ly/ly/words.py to online documentation')
        parser.add_argument('-u', '--document-url', help='the URL of the LilyPond index commands document. '
                                                         'If absent, a default is used')
        parser.add_argument('-w', '--words-path', help='the path to your local python-ly/ly/words.py. '
                                                       'If absent, a default is used')
        args = parser.parse_args()

        if args.document_url:
            self.lilypond_index_url = args.document_url
        else:
            print("Using LilyPond Doc :", self.lilypond_index_url)

        if args.words_path:
            self.python_ly_words_path = args.words_path
        else:
            print("Using words.py path:", self.python_ly_words_path)

    def get_python_ly_words_list(self, words_path: str) -> set:
        """Search words.py for words that are like 'foo', and return a set of words"""
        with open(words_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        words = set()
        pattern = re.compile(self.find_quoted_word)  # find line that looks like 'foo',

        for line in lines:
            matcher = pattern.match(line)
            if matcher:
                words.add(matcher.group(1))

        return words

    def main(self):
        """Compare words from LilyPond index online to python-ly/ly/words.py"""
        self.get_args()
        index_text = get_text_from_html(self.lilypond_index_url)
        words_list = self.get_python_ly_words_list(self.python_ly_words_path)

        for line in index_text.splitlines():  # the web page lines
            # line must start with any number of whitespace characters, then a backslash
            if re.match(r'\s*\\', line):
                found = False
                for word in words_list:  # words.py words
                    # match any number of spaces, a backslash, the word, and some kind of word boundary
                    if re.match(r"\s*\\" + re.escape(word) + r"\b", line):
                        found = True
                        break

                # We got all the way through the words list without a match, so this word is missing
                if not found:
                    print(line)


if __name__ == '__main__':
    CompareLilyPondToWords().main()
