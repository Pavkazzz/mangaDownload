from grab import Grab
from chapter import download_chapter
from optparse import OptionParser


def download_manga(link, path, zipping_type):
    g = Grab()
    g.go(link, log_file="manga.html")

    for item in g.doc.select('//div[@class="expandable chapters-link"]//table//a/@href'):
        chapter = link[:link.rfind('/')] + item._node + '?mature=1'
        download_chapter(chapter, path, zip=zipping_type)


if __name__ == '__main__':

    parser = OptionParser(
        usage=" %prog http://www.readmanga.me/manganame [path]")
    parser.add_option("-l", "--link",
                      help="link to manga on http://www.readmanga.me \
                      or http://www.adultmanga.ru",
                      )
    parser.add_option("-f", "--file", default='~/Manga/',
                      help="destination folder", metavar="~/Manga/")

    parser.add_option("-t", "--type", default=False, help="format zipping type")

    (options, args) = parser.parse_args()
    zipping_type = options.__dict__.get('type')
    download_manga(args[0], options.__dict__.get('file'), zipping_type)
