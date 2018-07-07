import subprocess


def create_zip(path, zipping_type):
    try:
        if zipping_type == 'rar':
            subprocess.call(['rar', 'a', path+'.rar', path+'/', '-ep', '-m3'])
        if zipping_type == 'cbr':
            subprocess.call(['rar', 'a', path+'.cbr', path+'/', '-ep', '-m3'])
        elif zipping_type == 'zip':
            subprocess.call(['zip', '-r', '-j', path + '.zip', path + '/'])
        elif zipping_type == 'cbz':
            subprocess.call(['zip', '-r', '-j', path + '.cbz', path + '/'])
    except:
        pass
