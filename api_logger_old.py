#!/usr/bin/env python

import sys
import json
import time
import pprint
import datetime
from collections import defaultdict

import redis
import MySQLdb as mdb

import get_urls
import config

"""
Notes: commit after 1 minute
"""


try:
    con = mdb.connect(config.HOST, config.USER, config.PASSWORD, config.DB_NAME)
    cur = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS %s (
        DATE_TIME  DATETIME,
        STATUS  CHAR(5),
        URL VARCHAR(256),
        RESPONSE_TIME FLOAT,
        COUNT INT,
        PRIMARY KEY (DATE_TIME, STATUS, URL) )
        """ % (config.TABLE_RESPONSE)
    cur.execute(sql)

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    con.close()
    sys.exit(1)

#Redis connection
try:
    r = redis.Redis(
        host=settings['REDIS_SERVER'],
        port=settings['REDIS_PORT'])

except redis.ConnectionError:
    print('Redis Connection Error')

if __name__ == '__main__':
    fileBytePos = 0
    response_by_minute = defaultdict(dict)
    response_by_minute_count = defaultdict(dict)
    response_count = defaultdict(dict)
    tmp_time  = ''

    while True:
        inFile = open('./flask-timelog.txt','r')
        inFile.seek(fileBytePos)
        data = inFile.readline()
        
        if data[0].isdigit():
            i = data.split('::')
            rsp_time, rsp, url, date_time = i[0].strip(), i[1].split()[0], get_urls.process_url(i[3]), i[-1].split('.')[0][:-3].strip()
            #defaultdict initialize if key already not there
            if not response_by_minute.get(date_time, {}).get(rsp):
                response_by_minute[date_time][rsp] = defaultdict(dict)
                response_by_minute_count[date_time][rsp] = defaultdict(int)

            response_by_minute[date_time][rsp][url] = response_by_minute.get(date_time,{}).get(rsp,{}).get(url,0) + float("{0:.4f}".format(float(rsp_time.split(':')[-1])))
            #stores count of url with status in 1 minute period
            response_by_minute_count[date_time][rsp][url] += 1
            response_count[url][rsp] = response_count.get(url, {}).get(rsp, 0) + 1
            cur.execute('INSERT INTO API_PERFORM_TEST (DATE_TIME, STATUS, URL, RESPONSE_TIME, COUNT) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE RESPONSE_TIME =  VALUES(RESPONSE_TIME), COUNT =  VALUES(COUNT)', (date_time, rsp, url, response_by_minute[date_time][rsp][url], response_by_minute_count[date_time][rsp][url]))
            if tmp_time != date_time:
                con.commit();
                tmp_time = date_time

        fileBytePos = inFile.tell()
        inFile.close()
        #for development remove it once deployed
        print('current: {0} -> {1}'.format(fileBytePos, 386440877) )
        if fileBytePos >= 386440877:
            break

    with open('api_perform', 'w') as o:
        json.dump(response_by_minute, o)
    with open('api_status', 'w') as b:
        json.dump(response_count, b)