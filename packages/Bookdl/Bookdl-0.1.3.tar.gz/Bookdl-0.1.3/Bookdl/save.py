import requests
import re
import sys
import os
from . import logger
from termcolor import colored
import time

logger = logger.logger()


def save(title, url):
    '''Function to save the file in downloads directory.'''

    try:
        extension = re.findall('.*ext=(.*)', url)
        extension = '.' + extension[0].strip(' ')
    except Exception as e:
        logger.debug(e)
        extension = ".pdf"

    home = os.path.expanduser("~")
    logger.debug(home)
    Books = os.path.join(home, "Books/")
    if not os.path.exists(Books):
        os.makedirs(Books)
    path = Books + title + extension
    if check(path):
        with open(path, 'wb') as f:
            try:
                response = requests.get(url, stream=True)
            except Exception as e:
                logger.debug(e)
                print("file not found!")
                sys.exit()

            total = response.headers.get('content-length')
            size = int(total) / (1024 * 1024)
            size = round(size, 2)
            if total is None:
                f.write(response.content)
            else:
                progress_bar(title, total, path, response, f)
    else:
        print("No changes were made.")


def progress_bar(title, total, path, response, f):
    '''Function to display the progress of download'''

    print(f"Downloading {colored(title, 'green', attrs = ['bold'])}")
    print(f"saving the file to: {path}")
    logger.debug(path)
    downloaded = 0
    total = int(total)
    chunk = max(int(total / 1000), 1024 * 1024)
    start = time.time()
    for data in response.iter_content(chunk_size=chunk):
        downloaded += len(data)
        downloaded_size = downloaded / (1024 * 1024)
        downloaded_size = round(downloaded_size, 2)
        speed = downloaded_size / (time.time() - start)
        eta = int((total - downloaded) / (speed * 1024 * 1024))
        if(speed > 1):
            speed = int(speed)
            speed = str(speed) + ' m'
        else:
            speed = int(speed * 1024)
            speed = str(speed) + ' k'
        done = int(50 * downloaded / total)
        details = "{} mb | {}bps |".format(int(downloaded_size), speed)
        completed = '▇' * done
        remaining = '░' * (50 - done)
        bar = " |{}{}|".format(completed, remaining)
        bar = colored(bar, "cyan")
        percent = done * 2
        f.write(data)
        progress = "\r {} {}s {}{}%".format(details, eta, bar, percent)
        sys.stdout.write(progress)
        sys.stdout.flush()

    sys.stdout.write('\n')
    print("File saved.")


def check(path):
    if os.path.exists(path):
        warning = "File already exists! Do you want to overwrite it?(y/n)"
        logger.warning(warning)
        choice = input()
        logger.debug(choice)
        return True if choice == 'y' else False
    else:
        return True
