
import sys
import pytz
import json
import random
import pprint
from datetime import datetime, time

import MySQLdb as mdb
import pygal
from pygal.style import NeonStyle, DarkGreenStyle, LightGreenStyle, DarkColorizedStyle
from flask import Flask, Response , render_template, request

import config


app = Flask(__name__ , static_url_path='')

try:
    con = mdb.connect(config.HOST, config.USER, config.PASSWORD, config.DB_NAME)
    cur = con.cursor()

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    con.close()
    sys.exit(1)


two0 = []
#three1 = []
three2 = []
four0 = []
four3 = []
four4 = []
four9 = []
five0 = []
d = json.load(open('api_perform'))
api_status = json.load(open('api_status'))
i = sorted(d.keys())
C = 0

@app.route('/')
def index():
    """ to render figures on html """
    return render_template('index.html')

@app.route('/user/details/others/')
def user_details_others():
    return render_template('user_details_others.html')


@app.route('/timeline/user/')
def timeline_user():
    return render_template('timeline_user.html')


@app.route('/get/pie/<par1>/')
@app.route('/get/pie/<par1>/<par2>/')
@app.route('/get/pie/<par1>/<par2>/<par3>/')
def get_pie(par1='', par2='', par3=''):

    url = 'http://api.frankly.me' + '/' + par1 + '/' + par2 + '/' + par3 + '/'
    url = url.strip('/')
    status = api_status[url]

    pie_chart = pygal.Pie(style=DarkColorizedStyle, inner_radius=.4)
    pie_chart.title = 'API Status'
    for k, v in status.iteritems():
        pie_chart.add(k, v)
    return Response(response=pie_chart.render(), content_type='image/svg+xml')


@app.route('/get/<par1>/')
@app.route('/get/<par1>/<par2>/')
@app.route('/get/<par1>/<par2>/<par3>/')
def get_line(par1='', par2='', par3=''):

    global C 
    C += 1

    url = 'http://api.frankly.me' + '/' + par1 + '/' + par2 + '/' + par3 + '/'
    url = url.strip('/')

    try:
        #cur.execute("SELECT * FROM API_PERFORM where status=200 and url='%s' order by date_time desc LIMIT 10" % (url))
        data = []
        for status in config.STATUS:
            cur.execute('select date_time, response_time FROM API_PERFORM where status=%s and url="%s" and DATE_TIME BETWEEN "2015-8-5 13:28" AND "2015-8-5 13:38" order by date_time desc LIMIT 10' % (status, url))
            #cur.execute(sql)
            data.append(cur.fetchall())
        #DATE_TIME BETWEEN '2015-8-5 13:37' AND '2015-8-5 13:38'
        #data200 = [(k[0].time(), k[1]) for k in cur.fetchall()]
        print data
    except Exception as e:
        print(e)

    two0.append((datetime.strptime(i[C], '%Y-%m-%d %H:%M').time(), d[i[C]].get('200', {url: 0}).get(url, 0)))
    #three1.append((datetime.strptime(i[C], '%Y-%m-%d %H:%M').time(), d[i[C]].get('301', {url: 0}).get(url, 0)))
    three2.append((datetime.strptime(i[C], '%Y-%m-%d %H:%M').time(), d[i[C]].get('302', {url: 0}).get(url, 0)))
    four0.append((datetime.strptime(i[C], '%Y-%m-%d %H:%M').time(), d[i[C]].get('400', {url: 0}).get(url, 0)))
    four3.append((datetime.strptime(i[C], '%Y-%m-%d %H:%M').time(), d[i[C]].get('403', {url: 0}).get(url, 0)))
    four4.append((datetime.strptime(i[C], '%Y-%m-%d %H:%M').time(), d[i[C]].get('404', {url: 0}).get(url, 0)))
    four9.append((datetime.strptime(i[C], '%Y-%m-%d %H:%M').time(), d[i[C]].get('409', {url: 0}).get(url, 0)))
    five0.append((datetime.strptime(i[C], '%Y-%m-%d %H:%M').time(), d[i[C]].get('500', {url: 0}).get(url, 0)))

    timeline = pygal.TimeLine(
    x_label_rotation=35, truncate_label=-1,
    x_value_formatter=lambda dt: dt.strftime('%H:%M'), 
    dots_size=5, legend_box_size=15, label_font_size=34, 
    style=NeonStyle, fill=True, x_title='Time')

    timeline.title = 'API Performance'
    
    """
    dateline.add("Serie", [
    (time(), 0),
    (time(6), 5),
    (time(8, 30), 12),
    (time(11, 59, 59), 4),
    (time(18), 10),
    (time(23, 30), -1),
    ])
    """
    """
    timeline.add(config.STATUS[0], two0)
    timeline.add(config.STATUS[1], three2)
    timeline.add(config.STATUS[2], four0)
    timeline.add(config.STATUS[3], four3)
    timeline.add(config.STATUS[4], four4)
    timeline.add(config.STATUS[5], four9)
    timeline.add(config.STATUS[6], five0)
    """
    for l in range(len(config.STATUS)):
        timeline.add(config.STATUS[l], data[l])

    if len(two0) >= 10:
        two0.pop(0)
        three2.pop(0)
        four0.pop(0)
        four3.pop(0)
        four4.pop(0)
        four9.pop(0)
        five0.pop(0)

    return Response(response=timeline.render(), content_type='image/svg+xml')

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run('0.0.0.0',5000)




"""
Top URLs with 500+ requests

[u'http://api.frankly.me/timeline/user',
 u'http://api.frankly.me/utils/install_ref',
 u'http://api.frankly.me/server/update_video_state',
 u'https://api.frankly.me/image/resize',
 u'http://api.frankly.me/notifications/count',
 u'http://api.frankly.me/image/resize',
 u'http://api.frankly.me/videoview',
 u'http://api.frankly.me/list/items',
 u'http://api.frankly.me/appversion',
 u'http://api.frankly.me/remote/get',
 u'http://api.frankly.me/user/profile',
 u'http://api.frankly.me/update/push_id',
 u'http://api.frankly.me/login/email',
 u'http://api.frankly.me/user/details',
 u'http://api.frankly.me/notification/seen',
 u'http://api.frankly.me/app/welcome/users',
 u'http://api.frankly.me/mixpanel/trackswitch',
 u'http://api.frankly.me/list/feed',
 u'http://api.frankly.me/channel/feed',
 u'http://api.frankly.me/slug',
 u'http://api.frankly.me/user/follow/multiple',
 u'http://api.frankly.me/user/details/others',
 u'http://api.frankly.me/getnotifications',
 u'http://api.frankly.me/list/featured/users']
"""