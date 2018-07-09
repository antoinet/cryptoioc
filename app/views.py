#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from functools import reduce
from app import app
from app.models import Pool
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/browse')
def browse():
    pools = Pool.read_pools('pools.csv')
    pools = [x for x in pools if x.dns_cache]
    count = reduce(lambda s, p: s + len(p.dns_cache.ips.split(',')), pools, 0)
    return render_template('browse.html', count=count, pools=pools)

@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/json')
def api_json():
    pools = Pool.read_pools('pools.csv')
    result = []
    for pool in [x for x in pools if x.dns_cache]:
        result.append({
            'domain': pool.domain,
            'port': pool.port,
            'currency': pool.currency,
            'comment': pool.comment,
            'ips': pool.dns_cache.ips.split(','),
            'timestamp': pool.dns_cache.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utf-8'}
