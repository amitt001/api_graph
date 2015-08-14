import sys
import pytz
import json
import random
import pprint
from datetime import datetime, time

import MySQLdb as mdb
import pygal
from pygal.style import NeonStyle, DarkGreenStyle, LightGreenStyle, DarkColorizedStyle, CleanStyle
from flask import Flask, Response , render_template, request

import config


app = Flask(__name__ , static_url_path='')

#MySQL server connection
try:
    con = mdb.connect(config.HOST, config.USER, config.PASSWORD, config.DB_NAME)
    cur = con.cursor()
except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    con.close()
    sys.exit(1)


@app.route('/')
def index():
    """ to render figures on html """
    return render_template('index.html')

@app.route('/user/details/others/')
def user_details_others():
    return render_template('index.html', 
        src='/get' + request.path, 
        src_pie='/get/pie' + request.path)

@app.route('/question/list/public/')
def question_list_public():
    return render_template('index.html', 
        src='/get' + request.path, 
        src_pie='/get/pie' + request.path)

@app.route('/list/trending/users/')
def list_trending_users():
    return render_template('index.html', 
        src='/get' + request.path, 
        src_pie='/get/pie' + request.path)

@app.route('/question/view/')
def question_view():
    return render_template('index.html', 
        src='/get' + request.path, 
        src_pie='/get/pie' + request.path)

@app.route('/timeline/user/')
def timeline_user():
    return render_template('index.html', 
        src='/get' + request.path, 
        src_pie='/get/pie' + request.path)


@app.route('/get/pie/<par1>/')
@app.route('/get/pie/<par1>/<par2>/')
@app.route('/get/pie/<par1>/<par2>/<par3>/')
def get_pie(par1='', par2='', par3=''):
    url = 'http://api.frankly.me' + '/' + par1 + '/' + par2 + '/' + par3 + '/'
    url = url.strip('/')
    sql = 'select status, count from %s where DATE_TIME BETWEEN "2015-8-5 13:28" AND "2015-8-5 13:38" and url="%s"' % (config.TABLE_RESPONSE, url)
    cur.execute(sql)
    data = cur.fetchall()

    status_dict = {}
    for k,v in data:
        status_dict[k] = status_dict.get(k, 0) + v

    pie_chart = pygal.Pie(style=CleanStyle, inner_radius=.4)
    pie_chart.title = 'API Status'

    for key, value in status_dict.iteritems():
        pie_chart.add(key, value)
        
    return Response(response=pie_chart.render(), content_type='image/svg+xml')


@app.route('/get/<par1>/')
@app.route('/get/<par1>/<par2>/')
@app.route('/get/<par1>/<par2>/<par3>/')
def get_line(par1='', par2='', par3=''):

    url = 'http://api.frankly.me' + '/' + par1 + '/' + par2 + '/' + par3 + '/'
    url = url.strip('/')
    print url

    try:
        data = []
        for status in config.STATUS:
            cur.execute('select date_time, response_time FROM %s where status=%s and url="%s" and DATE_TIME BETWEEN "2015-8-5 13:28" AND "2015-8-5 13:38" order by date_time desc LIMIT 10' % (config.TABLE_RESPONSE , status, url))
            data.append(cur.fetchall())

    except Exception as e:
        print(e)

    timeline = pygal.TimeLine(
    x_label_rotation=35, truncate_label=-1,
    x_value_formatter=lambda dt: dt.strftime('%H:%M'), 
    dots_size=5, legend_box_size=15, label_font_size=34, 
    style=CleanStyle, fill=True, x_title='Time')

    timeline.title = 'API Performance'

    for l in range(len(config.STATUS)):
        timeline.add(config.STATUS[l], data[l])

    return Response(response=timeline.render(), content_type='image/svg+xml')

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run('0.0.0.0',5000)