# coding=utf-8

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


def download_chapter(link, path, manga_name=None, zip=False):
    g = Grab()
    g.go(link)
    chapter_name = g.doc.select(
        '//a[@href="#header"][@property="v:title"]/text()')
    # print chapter_name.text()
    if not manga_name:
        manga_name = g.doc.select('//a[@class="manga-link"]/text()')

    current_path = os.path.join(path, manga_name.text())
    current_path = os.path.join(current_path, chapter_name.text())
    current_path = os.path.expanduser(current_path)
    # Hack for windows
    current_path = current_path.replace('.', '')

    if os.path.isdir(current_path) or os.path.isfile(current_path + '.rar'):
        return 0
    else:
        try:
            os.makedirs(current_path)
        except os.error:
            pass

    img_list = re.findall(
        'http:\/\/[\w+]{1,2}\.[\w\.\/\-]+\.[jpgJPGnNgifGIF]{3}',
        g.response.body)

    processlist = []
    for img in img_list:
        img_name = img[img.rfind('/') + 1:]
        processlist.append(
            multiprocessing.Process(target=worker,
                                    args=(img, current_path, img_name)))

    for proc in processlist:
        proc.start()

    for proc in processlist:
        proc.join()

    if zip:
        create_zip(current_path)
        shutil.rmtree(current_path)


if __name__ == '__main__':
    download_chapter('http://readmanga.me/naruto/vol71/690', '~/Manga')
