from grab import Grab
import re
import os
import multiprocessing
import requests
from zip import create_zip
import shutil




def worker(link, path, img_name):
    p = requests.get(link)
    out = open(os.path.join(path, img_name), "wb")
    out.write(p.content)
    out.close()




def download_chapter(link, manga_name=None):
    g = Grab()
    g.go(link)
    chapter_name = g.doc.select('//a[@href="#header"][@property="v:title"]/text()')
    print chapter_name.text()
    if not manga_name:
        manga_name = g.doc.select('//a[@class="manga-link"]/text()')

    #print chapter_name.text() manga_name.text()



    path = '~/Manga/%s/%s' % (manga_name.text(), chapter_name.text())
    path = os.path.expanduser(path)

    if os.path.isdir(path) or  os.path.isfile(path+'.rar'):
        return 0
    else:
        try:
            os.makedirs(path)
        except os.error:
            pass


    img_list = re.findall('http:\/\/[\w+]{1,2}\.[\w\.\/\-]+\.[jpgJPGnNgifGIF]{3}', g.response.body)

    processlist = []
    for img in img_list:
        #print img[img.rfind('/')+1:]
        img_name = img[img.rfind('/')+1:]
        processlist.append(multiprocessing.Process(target=worker, args=(img, path, img_name)))

    for proc in processlist:
        proc.start()

    for proc in processlist:
        proc.join()

    create_zip(path)
    shutil.rmtree(path)




if __name__ == '__main__':
    download_chapter('http://adultmanga.ru/sankarea/vol7/34?mature=1')