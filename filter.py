#!/usr/bin/env python

import csv
import dns.resolver
import json

rules = {}
reverse_rules = {}
with open('pools.csv', 'rb') as csvfile:
    poolreader = csv.reader(csvfile, delimiter=',')
    for row in poolreader:
        domain = row[0]
        port = row[1]
        currency = row[2]
        answers = dns.resolver.query(domain, 'A')
        ips = [str(ip) for ip in answers]
        if not rules.get(currency):
            rules[currency] = []
        rules[currency].append('(dst ip in [%s] and proto tcp and port %s)' % (', '.join(ips), port))
        for ip in answers:
            key = "%s:%s" % (ip, port)
            reverse_rules[key] = "currency: %s, pool: %s:%s" % (currency, domain, port)
 
for k in rules.keys():
    print '=== ' + k
    print " or\n".join(rules[k])
    print

print
print "-------------"
print

print json.dumps(reverse_rules, indent=4, separators=(',', ': '))

