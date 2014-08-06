import subprocess


def create_zip(path):
    subprocess.call(['rar', 'a', path+'.rar', path+'/', '-ep', '-m3'])
