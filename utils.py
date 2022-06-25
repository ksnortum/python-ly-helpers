# This program is protected by the Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
# (https://creativecommons.org/licenses/by-sa/4.0/)

from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_description_list_text(soup: BeautifulSoup) -> str:
    """
    When getting text from an HTML document, some terms can be in "dl" elements.  This will mean
    that the term and its description will be on separate lines.  This utility combines the term
    and its description, separated them with a tab character.
    """
    dl_text = ''

    for dls in soup.find_all('dl'):
        dts = [term.text for term in dls.find_all('dt')]
        dds = [description.text for description in dls.find_all('dd')]

        for term, description in zip(dts, dds):
            dl_text += term + '\t' + description

    return dl_text


def get_table_text(soup: BeautifulSoup) -> str:
    """
    When getting text from an HTML document, the text from an adjacent cell may be concatenated together.
    To deal with this, this function goes through all table rows and finds the cells.  Then it puts the
    row back together with a tab character between cells.
    """
    table_text = ''

    for table in soup.find_all('table'):
        for tr in table.find_all('tr'):
            row_text = ''
            for td in tr.find_all('td'):
                row_text += td.get_text() + '\t'
            table_text += row_text + '\n'

    return table_text


def get_text_from_html(url: str) -> str:
    """
    Get lines of text from a web page.  Tables and "dl" elements are processed for readability.
    """
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    table_text = get_table_text(soup)
    dl_text = get_description_list_text(soup)

    # kill all script and style and table and dl elements
    # - script and style: because we don't want to search through that text
    # - table and dl: because we've already processed those elements
    for script in soup(("script", "style", "table", "dl")):
        script.extract()  # rip it out

    return soup.getText() + '\n' + table_text + '\n' + dl_text
