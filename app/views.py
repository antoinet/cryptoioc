#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import io
import csv
from functools import reduce
from app import app
from app.models import Pool
from flask import render_template
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/browse')
def browse():
    pools = Pool.read_pools('pools.csv')
    count = reduce(lambda s, p: s + len(p.dns_cache.ips.split(',')), pools, 0)
    return render_template('browse.html', count=count, pools=pools)

@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/downloads/ids')
def api_ids():
    header = """\
################################################################
# CryptoIOC database dump                                      #
# Last updated: {date} (UTC)                      #
################################################################
"""
    pools = Pool.read_pools('pools.csv')
    template = 'alert tcp $HOME_NET any -> {ip} {port} (msg:"CryptoIOC mining pool traffic detected, domain: {domain},'\
               ' currency: {currency}"; flow:established,from_client; sid:{sid}; rev:1;)'
    result = []
    sid = 1000001
    most_recent = datetime.fromtimestamp(0)
    for p in pools:
        for ip in p.dns_cache.ips.split(','):
            result.append(template.format(ip=ip, port=p.port, domain=p.domain, currency=p.currency, sid=sid))
            sid += 1
        if p.dns_cache.timestamp > most_recent:
            most_recent = p.dns_cache.timestamp
    return header.format(date=most_recent.strftime(DATE_FORMAT)) + '\n'.join(result), 200, {'Content-Type': 'text/plain'}

@app.route('/downloads/csv')
def api_csv():
    header = """\
################################################################
# CryptoIOC for Suricata                                       #
# Last updated: {date} (UTC)                      #
################################################################
# domain,ipaddress,tcpport,currency,comment,lastupdated
"""
    pools = Pool.read_pools('pools.csv')
    rows = []
    most_recent = datetime.fromtimestamp(0)
    for p in pools:
        for ip in p.dns_cache.ips.split(','):
            rows.append([p.domain, ip, p.port, p.currency, p.comment, p.dns_cache.timestamp.strftime(DATE_FORMAT)])
            if p.dns_cache.timestamp > most_recent:
                most_recent = p.dns_cache.timestamp
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerows(rows)
    return header.format(date=most_recent.strftime(DATE_FORMAT)) + output.getvalue(), 200, {'Content-Type': 'text/plain'}

@app.route('/downloads/netflow')
def api_netflow():
    header = """\
################################################################
# CryptoIOC NetFlow profile                                    #
# Last updated: {date} (UTC)                      #
################################################################
#
"""
    pools = Pool.read_pools('pools.csv')
    domains = {}
    most_recent = datetime.fromtimestamp(0)
    for p in pools:
        if p.domain not in domains:
            domains[p.domain] = [p]
        else:
            domains[p.domain].append(p)
        if p.dns_cache.timestamp > most_recent:
            most_recent = p.dns_cache.timestamp
    rules = []
    for domain, poollist in domains.items():
        ports = ','.join([p.port for p in poollist])

        rules.append('(dst ip in [%s] and proto tcp and port in [%s])' % (poollist[0].dns_cache.ips, ports))
    return header.format(date=most_recent.strftime(DATE_FORMAT)) + ' or\n'.join(rules), 200, {'Content-Type': 'text/plain'}

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/json')
def api_json():
    pools = Pool.read_pools('pools.csv')
    result = []
    for pool in pools:
        result.append({
            'domain': pool.domain,
            'port': pool.port,
            'currency': pool.currency,
            'comment': pool.comment,
            'ips': pool.dns_cache.ips.split(','),
            'timestamp': pool.dns_cache.timestamp.strftime(DATE_FORMAT)
        })
    return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utf-8'}
