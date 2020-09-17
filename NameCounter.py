from bs4 import BeautifulSoup
import json


class NameCounter:
    def __init__(self, raw_htmls):
        self.names = []
        self.raw_htmls = raw_htmls
        self.title = None

    def parse_and_save(self):
        for raw_html in self.raw_htmls:
            self.parse_per_page(raw_html)

        res = {
            'title': self.title,
            'total_responses': len(self.names),
            'names': self.names
        }

        with open(f'./results/{self.title}.json', 'w+') as fh:
            fh.write(json.dumps(res))

        print(f'Total {len(self.names)} Threads saved for {self.title}.')

    def parse_per_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        if not self.title:
            self.title = soup.select('h1')[0].text
        tags = soup.select('div.d2l-textblock-secondary')
        for tag in tags:
            text = tag.text
            if not text or text == "•":
                continue
            name = text.split('posted')[0].strip()
            self.names.append(name)
