from grab import Grab
from Chapter import download_chapter

def download_manga(link):
    g = Grab()
    g.go(link)
    for item in g.doc.select('//table[@id="chapters-list"]//a/@href'):
        chapter = link[:link.rfind('/')] + item.node + '?mature=1'
        download_chapter(chapter)




if __name__ == '__main__':
    download_manga('http://adultmanga.ru/sankarea')