#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app

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
    result = []
    with open('pools.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            domain,port,currency,comment = row
            answers = dns.resolver.query(domain, 'A')
            ips = [str(ip) for ip in answers]
            result.append("%s: %s" % (domain, ','.join(ips)))
    return '<br/>'.join(result)
