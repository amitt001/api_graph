#!/usr/bin/env python

import sys
import json
import time
import pprint
import datetime
from collections import defaultdict

import redis
from flask import Flask, jsonify

import get_urls
import config

app = Flask(__name__ , static_url_path='')


#Redis connection
try:
    r = redis.Redis(
        host=config.REDIS_SERVER,
        port=config.REDIS_PORT)
except redis.ConnectionError:
    print('Redis Connection Error')

@app.route('/')
def index():
    return 'Online'

@app.route('/get/log')
@app.route('/get/log/')
def get_logs():
    fileBytePos = 0
    data_count = 500
    response_by_minute = defaultdict(dict)
    response_by_minute_count = defaultdict(dict)
    response_count = defaultdict(dict)
    tmp_time  = 'null'
    #save file byte position in Redis if already exists get position
    while True:
        inFile = open('./flask-timelog.txt','r')
        if not r.hget(config.REDIS_HNAME, 'fileBytePos'):
            r.hset(config.REDIS_HNAME, 'fileBytePos', fileBytePos)
        fileBytePos = int(r.hget(config.REDIS_HNAME, 'fileBytePos'))

        inFile.seek(fileBytePos)
        data = inFile.readline()
        if data[0].isdigit():
            i = data.split('::')
            rsp_time, rsp, url, date_time = i[0].strip(), i[1].split()[0], get_urls.process_url_new(i[3]), i[-1].split('.')[0][:-3].strip()

            if tmp_time == 'null':
                tmp_time = date_time

            if tmp_time != date_time:
                break
                
            #defaultdict initialize if key already not there
            if not response_by_minute.get(date_time, {}).get(rsp):
                response_by_minute[date_time][rsp] = defaultdict(dict)
                response_by_minute_count[date_time][rsp] = defaultdict(int)

            response_by_minute[date_time][rsp][url] = response_by_minute.get(date_time,{}).get(rsp,{}).get(url,0) + float("{0:.4f}".format(float(rsp_time.split(':')[-1])))
            #stores count of url with status in 1 minute period
            response_by_minute_count[date_time][rsp][url] += 1
            response_count[url][rsp] = response_count.get(url, {}).get(rsp, 0) + 1

        fileBytePos = inFile.tell()
        r.hset(config.REDIS_HNAME, 'fileBytePos', fileBytePos)
        inFile.close()

        data_count -= 1

    return jsonify({'log_by_min': response_by_minute, 'log_by_count': response_by_minute_count}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8000)
