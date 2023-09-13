import queue
import requests
import threading
import sys
from fake_useragent import UserAgent

ua = UserAgent()

AGENT = ua.random
EXTENSIONS = ['.php', '.bak', '.origin', '.inc']
TARGET = ''
THREADS = 10
WORDLIST = 'SVNDigger/all.txt'


def get_words(resume=None):

    def extend_words(word):
        if '.' in word:
            words.put(f'/{word}')
        else:
            words.put(f'/{word}/')

        for extension in EXTENSIONS:
            words.put(f'{word}{extension}')

    with open(WORDLIST) as file:
        raw_words = file.read()

    found_resume = False
    words = queue.Queue()
    for word in raw_words.split():
        if resume is not None:
            if found_resume:
                extend_words(word)
            elif word == resume:
                found_resume = True
                print(f'Resuming wordlist from: {resume}')
        else:
            print(word)
            extend_words(word)
    return words


def dir_bruter(words):
    headers = {'User-Agent': AGENT}
    while not words.empty():
        url = f'{TARGET}{words.get()}'

        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            sys.stderr.write('-')
            sys.stderr.flush()
            continue

        if r.status_code == 200:
            print(f'Success {r.status_code}: {url}')
        elif r.status_code == 404:
            sys.stderr.write('.')
            sys.stderr.flush()
        else:
            print(f'{r.status_code} {url}')


def main():
    words = get_words()
    sys.stdin.readline()
    for _ in range(THREADS):
        t = threading.Thread(target=dir_bruter, args=(words, ))
        t.start()


if __name__ == '__main__':
    main()
