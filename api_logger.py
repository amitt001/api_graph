#!/usr/bin/env python

import sys
import json
import time
import pprint
import datetime
from collections import defaultdict

import MySQLdb as mdb

import get_urls


#urls = json.load(open('urls', 'r')).keys()

try:
    con = mdb.connect('localhost', 'amit', 'pass', 'testdb');
    cur = con.cursor()
    #{"2015-08-06 09:05": {"200": {"http://api.frankly.me/timeline/user": 6964.552999999999
    sql = """CREATE TABLE IF NOT EXISTS API_PERFORM (
        DATE_TIME  DATETIME,
        STATUS  CHAR(5),
        URL VARCHAR(256),
        RESPONSE_TIME FLOAT,
        COUNT INT,
        PRIMARY KEY (DATE_TIME, STATUS, URL) )
    """

    cur.execute(sql)

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    con.close()
    sys.exit(1)

if __name__ == '__main__':
    fileBytePos = 0
    minute_flg = 0
    response_by_minute = defaultdict(dict)
    response_by_minute_count = defaultdict(dict)
    response_count = defaultdict(dict)
    pp = pprint.PrettyPrinter()
    url_count = 0
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
            #cur.execute('REPLACE INTO API_PERFORM VALUES (%s, %s, %s, %s)', (date_time, rsp, url, response_by_minute[date_time][rsp][url]))
            cur.execute('INSERT INTO API_PERFORM (DATE_TIME, STATUS, URL, RESPONSE_TIME, COUNT) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE RESPONSE_TIME =  VALUES(RESPONSE_TIME), COUNT =  VALUES(COUNT)', (date_time, rsp, url, response_by_minute[date_time][rsp][url], response_by_minute_count[date_time][rsp][url]))
            con.commit();

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