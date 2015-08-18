
  ######################################################
 ##This module creates list of URLs from the log file##
######################################################

import json


urls = open('urls', 'r').read().splitlines()
urls.sort()

def process_url_new(url):
    url = url.split('?')[0].strip()
    if url in urls:
        return urls[urls.index(url)].strip()
    elif '/'.join(url.split('/')[:-1]) in urls:
        return urls[urls.index('/'.join(url.split('/')[:-1]))].strip()
    elif '/'.join(url.split('/')[:-2]) in urls:
        return urls[urls.index('/'.join(url.split('/')[:-2]))].strip()
    elif '/'.join(url.split('/')[:-3]) in urls:
        return urls[urls.index('/'.join(url.split('/')[:-3]))].strip()

    return url