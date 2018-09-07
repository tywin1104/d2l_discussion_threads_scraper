import sys
from NameCounter import NameCounter
from HtmlScraper import HtmlScraper

try:
    week = sys.argv[1]
except IndexError:
    raise Exception('Must provide week number to get M&Ms from')


def main():
    scraper = HtmlScraper(week=week)
    scraper.start()

    counter = NameCounter(scraper.htmls)
    counter.parse()

main()
