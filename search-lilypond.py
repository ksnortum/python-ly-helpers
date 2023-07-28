import re
import argparse

from utils import get_text_from_html


class SearchLilyPond:
    """
    When updating python-ly/ly/words.py with new commands, it's sometimes helpful to know the
    earliest version it is found on, or to get some more context of the word.  This class searches
    for a "raw" word (that is, unadorned) or with a backslash (\\\\) prepended and a word boundary
    at the end.  The changes, music functions, commands, and full index are searched from online
    documents.  The different versions that a checked ar in the "versions" tuple.
    """

    templates = {
        'changes': "https://lilypond.org/doc/{}/Documentation/changes/index#top",
        'functions': "https://lilypond.org/doc/{}/Documentation/notation/available-music-functions",
        'commands': "https://lilypond.org/doc/{}/Documentation/notation/lilypond-command-index",
        'index': "https://lilypond.org/doc/{}/Documentation/notation/lilypond-index",
    }
    versions = ('v2.25', 'v2.24', 'v2.22', 'v2.20', 'v2.18', 'v2.16', 'v2.14')

    @staticmethod
    def get_arguments() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='Searches through the LilyPond documentation online '
                                                     'for a command')
        parser.add_argument('search_string', help='the string to search for in the documentation')
        parser.add_argument('-i', '--interactive', help='run interactively (enter anything as search_string)',
                            action="store_true")
        parser.add_argument('-w', '--word', help='prepend a backslash (\\) and end with a word boundary, '
                                                 'default is True', action="store_true", default=True)
        parser.add_argument('-r', '--raw', help='search for this string exactly (no slash or word boundaries)',
                            action="store_true")
        parser.add_argument("-v", "--verbosity", action="count", help="print the URL that the data comes from")
        args = parser.parse_args()

        if args.interactive:
            args.search_string = input("Enter a string to search the documentation by: ")

        return args

    def main(self) -> None:
        args = self.get_arguments()
        search_for_this = args.search_string

        # search string with a backslash prepended and ending on a word boundary, unless raw
        if not args.raw:
            search_for_this += r'\b'
            if not search_for_this.startswith('\\'):
                search_for_this = '\\\\' + search_for_this

        if args.verbosity:
            print("Search term:", search_for_this)

        for name, html_template in self.templates.items():
            print(f'*** Searching {name}...')

            for version in self.versions:
                url = html_template.format(version)
                text = get_text_from_html(url)

                # break html text into lines and remove leading and trailing spaces while searching for text
                found = [line.strip() for line in text.splitlines()
                         if re.search(search_for_this, line) is not None]

                if found:
                    print("---", version, end=' ')
                    if args.verbosity:
                        print('(' + url + ')', end='')
                    print()
                    print(*found, sep='\n')


if __name__ == '__main__':
    SearchLilyPond().main()
