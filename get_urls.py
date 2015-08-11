
  ######################################################
 ##This module creates list of URLs from the log file##
######################################################

import json


def process_url(url):
    #url = url.split('::')[3]
    url = url.split('?')[0].strip()
    if '/user/profile/' in url or '/list/public/' in url or '/question/downvote/' in url or '/karaoke/tracks/' in url or '/question/upvote/' in url or '/question/view/' in url or '/user/update_profile/' in url or '/post/view/' in url or '/dubs/audiocategories/' in url:
        url = '/'.join(url.split('/')[:-1])
    if '/multitype' in url:
        url = '/'.join(url.split('/')[:-2])
    if '/slug' in url:
        url = '/'.join(url.split('/')[:-2])
    if '/survey' in url:
        idx = url.split('/').index('survey')+1
        url = '/'.join(url.split('/')[:idx])

    return url