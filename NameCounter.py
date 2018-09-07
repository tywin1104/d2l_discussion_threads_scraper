from bs4 import BeautifulSoup


class NameCounter:
    def __init__(self, raw_htmls):
        # self.names = set()
        self.names = []
        self.raw_htmls = raw_htmls
        self.title = None

    def parse(self):
        for raw_html in self.raw_htmls:
            self.parse_per_page(raw_html)

        print(self.title)
        print('-----------')
        print(f'Total {len(self.names)} Threads')
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
                # self.names.add(name)
                self.names.append(name)
