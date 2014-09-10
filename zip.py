import subprocess


def create_zip(path):
    try:
        subprocess.call(['rar', 'a', path+'.rar', path+'/', '-ep', '-m3'])
    except:
        pass