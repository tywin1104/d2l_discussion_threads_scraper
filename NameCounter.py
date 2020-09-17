from bs4 import BeautifulSoup
from tempfile import NamedTemporaryFile
import shutil
import csv
import json
import os


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
        print('Updating target gradebook...')

        # Update CSV gradebook
        attendance = set()
        for name in self.names:
            # find match by first and last name with consistent order
            attendance.add(' '.join(sorted(name.split(' '))))


        temp_file = NamedTemporaryFile(mode='w', delete=False)

        with open(os.getenv('TARGET_GRADEBOOK'), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            writer = csv.writer(temp_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    writer.writerow(row)
                    line_count += 1
                    continue

                # assume row[1] and row[2] should be first/last names
                name_tokens = row[1].strip().split(' ') + row[2].strip().split(' ')
                name_identifier = " ".join(sorted(name_tokens))

                if name_identifier in attendance:
                    # assume 2nd last row is for M&M grading
                    # last row is reserved for D2L's generated End-of-Line Indicator
                    row[-2] = 1
                else:
                    row[-2] = 0

                writer.writerow(row)
                line_count += 1

        shutil.move(temp_file.name, os.getenv('TARGET_GRADEBOOK'))
        print(f'Processed {line_count} lines.')


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