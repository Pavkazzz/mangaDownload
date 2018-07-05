# coding=utf-8

from grab import Grab
import re
import os
import multiprocessing
import requests
from zip import create_zip
import shutil
from ast import literal_eval


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

    img_list = literal_eval(re.findall('\[\[.+\]\]', g.doc.body.decode('utf-8'))[0])
    img_one = []
    for image in img_list:
        img_one.append(image[1]+image[2])
    img_list = img_one
    del img_one

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


