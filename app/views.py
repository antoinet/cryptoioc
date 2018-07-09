#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from app import app
from app.models import Pool

@app.route('/hello')
def hello():
    return 'Hello, World!'


@app.route('/resolve/<domain>')
def resolve(domain):
    result = dns.resolver.query(domain, 'A')
    ips = [str(ip) for ip in result]
    app.logger.error(repr(result) + 'length: %s', len(ips))
    return 'resolving %s...<br/>' % domain + '<br/>'.join(ips)


@app.route('/test')
def test():
    pools = Pool.read_pools('pools.csv')
    result = []
    for pool in [x for x in pools if x.dns_cache]:
        result.append({
            'domain': pool.domain,
            'port': pool.port,
            'currency': pool.currency,
            'comment': pool.comment,
            'ips': pool.dns_cache.ips.split(','),
            'timestamp': pool.dns_cache.timestamp.strftime('%Y-%m-%d %H:%M:%s')
        })
    return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utf-8'}
