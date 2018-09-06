from bs4 import BeautifulSoup


# with open('test.html', 'r') as fh:
#     page_one_html = fh.read()

# with open('test1.html', 'r') as fh:
#     page_two_html = fh.read()

class NameCounter:

    def __init__(self, raw_htmls = [page_one_html, page_two_html]):
        self.names = set()
        self.raw_htmls = raw_htmls
        self.title = None

    def parse(self):
        for raw_html in self.raw_htmls:
            self.parse_per_page(raw_html)

        print(self.title)
        print('-----------')
        print(self.names)

    def parse_per_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        if not self.title:
            self.title = soup.select('h1')[0].text
        tags = soup.select('div.d2l-textblock-secondary')
        for tag in tags:
            if 'd2l-textblock-strong'not in tag.attrs['class']:
                sentence = tag.text
                # TODO : Could use Regx
                name = sentence.split('posted')[0].strip()
                self.names.add(name)
