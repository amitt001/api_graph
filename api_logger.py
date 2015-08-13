#!/usr/bin/env python

import sys
import json
import time
import datetime
import requests
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
        host=config.REDIS_SERVER,
        port=config.REDIS_PORT)

except redis.ConnectionError:
    print('Redis Connection Error')

tmp_count = 0

if __name__ == '__main__':
    while True:
        
        rsp = requests.get(config.URL)
        response_by_minute = rsp.json()['log_by_min']
        response_by_minute_count = rsp.json()['log_by_count']

        for date_time in response_by_minute.keys():
            for rsp in response_by_minute[date_time].keys():
                for url, rsp_tym in response_by_minute[date_time][rsp].iteritems():
                    print (date_time, rsp, url, rsp_tym, response_by_minute_count[date_time][rsp][url])
                    cur.execute('INSERT INTO API_PERFORM_ONE (DATE_TIME, STATUS, URL, RESPONSE_TIME, COUNT) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE RESPONSE_TIME =  VALUES(RESPONSE_TIME), COUNT =  VALUES(COUNT)' , (date_time, rsp, url, rsp_tym, response_by_minute_count[date_time][rsp][url]))
                    
        con.commit()