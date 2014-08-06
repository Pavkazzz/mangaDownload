from grab import Grab
from Chapter import download_chapter
from optparse import OptionParser


def download_manga(link, path):
    g = Grab()
    g.go(link)
    for item in g.doc.select('//table[@id="chapters-list"]//a/@href'):
        chapter = link[:link.rfind('/')] + item.node + '?mature=1'
        download_chapter(chapter, path)




if __name__ == '__main__':

    parser = OptionParser(usage="$prog http://www.readmanga.me/manganame [path]")
    parser.add_option("-l", "--link",
                      help="link to manga on http://www.readmanga.me or http://www.adultmanga.ru",
                      )
    parser.add_option("-f", "--file", default='~/Manga/',
                      help="destination folder", metavar="~/Manga/")

    (options, args) = parser.parse_args()
    download_manga(args[0], options.__dict__.get('file'))
