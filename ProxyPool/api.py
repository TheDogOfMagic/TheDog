from flask import Flask, g

from db import RedisClient

import re
from setting import *


__all__ = ['app']

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'

@app.route('/random')
def random_proxy():
    """
    random a proxy
    return 随机代理（位置名）
    """
    conn = get_conn()
    return conn.random()

@app.route('/get')
def get_proxy():
    """
    get a proxy
    return 随机代理
    """
    conn = get_conn()
    results = conn.get()
    pattern = re.compile('(\d+\.\d+\.\d+\.\d+\:\d+)\(.*?\)')
    proxy = re.findall(pattern, results)
    return proxy[0]



@app.route('/count')
def get_counts():
    """
    Get the count of proxies
    return 代理池总量
    """
    conn = get_conn()
    return str(conn.count())

#代理池开关
app.PORXY_SWITCH = True

@app.route('/exit')
def exit_proxypool():
    app.PORXY_SWITCH = False
    return '<h2>Exit!.</h2>'

@app.route('/getexit')
def get_exit():
    return str(app.PORXY_SWITCH)

if __name__ == '__main__':
    app.run()
    