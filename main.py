
import pytz
import pygal
import json
import random
import pprint
from datetime import datetime, time
from pygal.style import NeonStyle, DarkGreenStyle, LightGreenStyle, DarkColorizedStyle
from flask import Flask, Response , render_template, request


app = Flask(__name__ , static_url_path='')

two0 = []
three1 = []
three2 = []
four0 = []
four3 = []
four4 = []
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
    #timeline = get_plot('user', 'details', 'others')
    #return Response(response=timeline.render(), content_type='image/svg+xml')
    return render_template('user_details_others.html')


@app.route('/timeline/user/')
def timeline_user():
    #timeline = get_plot('timeline', 'user')
    #return Response(response=timeline.render(), content_type='image/svg+xml')
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
    #Add Category and it's percentage in pie chart
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
    two0.append((datetime.strptime(i[C], '%Y-%m-%d %H:%M').time(), d[i[C]].get('200', {url: 0}).get(url, 0)))
    three1.append((datetime.strptime(i[C], '%Y-%m-%d %H:%M').time(), d[i[C]].get('301', {url: 0}).get(url, 0)))
    three2.append((datetime.strptime(i[C], '%Y-%m-%d %H:%M').time(), d[i[C]].get('302', {url: 0}).get(url, 0)))
    four0.append((datetime.strptime(i[C], '%Y-%m-%d %H:%M').time(), d[i[C]].get('400', {url: 0}).get(url, 0)))
    four3.append((datetime.strptime(i[C], '%Y-%m-%d %H:%M').time(), d[i[C]].get('403', {url: 0}).get(url, 0)))
    four4.append((datetime.strptime(i[C], '%Y-%m-%d %H:%M').time(), d[i[C]].get('404', {url: 0}).get(url, 0)))
    five0.append((datetime.strptime(i[C], '%Y-%m-%d %H:%M').time(), d[i[C]].get('500', {url: 0}).get(url, 0)))
    
    timeline = pygal.TimeLine(
    x_label_rotation=35, truncate_label=-1,
    x_value_formatter=lambda dt: dt.strftime('%H:%M'), 
    dots_size=5, legend_box_size=15, label_font_size=34, 
    style=NeonStyle, fill=True, x_title='Time')
    timeline.title = 'API Performance'

    timeline.add("200", two0)
    timeline.add("301", three1)
    timeline.add("302", three2)
    timeline.add("400", four0)
    timeline.add("403", four3)
    timeline.add("404", four4)
    timeline.add("500", five0)

    if len(two0) >= 10:
        two0.pop(0)
        three1.pop(0)
        three2.pop(0)
        four0.pop(0)
        four3.pop(0)
        four4.pop(0)
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