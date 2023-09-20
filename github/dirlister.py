import os


def run(**kwargs):
    files = os.listdir('.')
    return str(files)

