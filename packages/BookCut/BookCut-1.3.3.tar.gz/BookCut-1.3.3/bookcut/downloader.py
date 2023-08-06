import requests
from tqdm import tqdm
import os
from bs4 import BeautifulSoup as Soup


def downloading(link, name, author, file, destination_folder, type):
    '''finds the first available book and sends the link to file_downloader '''
    page = requests.get(link)
    soup = Soup(page.content, 'html.parser')

    searcher = [a['href'] for a in soup.find_all(href=True) if a.text]

    searcher_link = searcher[0]
    file_downloader(searcher_link, name, author, file, destination_folder, type)


def file_downloader(href, name, author, file, destination_folder, type):
    '''Downloads the book file to users folder'''
    response = requests.get(href, stream=True)
    total_size = int(response.headers.get('content-length'))
    inMb = total_size / 1000000
    inMb = round(inMb, 2)
    print("\nDownloading...", "\nTotal file size:", inMb, 'MB')

# Folder to download books
    filename = file
    if filename != "":
        pass
    else:
        filename = name + ' - ' + author + type
    path = destination_folder

    filename = os.path.join(path, filename)

    try:
        with open(filename, 'wb') as f:
            ''' For progress bar '''
            with tqdm(total=total_size, unit='iB',
                      unit_scale=True) as pbar:
                for ch in response.iter_content(chunk_size=1024):
                    if ch:
                        f.write(ch)
                        pbar.update(len(ch))

        print("================================\nFile saved as:", filename)
    except FileNotFoundError:
        print("ERROR! Is the destination folder exists? ")


def pathfinder():
    path = os.path.expanduser('~/Documents/BookCut')
    if os.path.isdir(path):
        pass
    else:
        os.makedirs(path)
    return path
