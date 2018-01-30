#!/usr/bin/env python

import csv
import dns.resolver

rules = {}
with open('pools.csv', 'rb') as csvfile:
    poolreader = csv.reader(csvfile, delimiter=',')
    for row in poolreader:
        answers = dns.resolver.query(row[0], 'A')
        ips = [str(ip) for ip in answers]
        if not rules.get(row[2]):
            rules[row[2]] = []
        rules[row[2]].append('(dst ip in [%s] and proto tcp and port %s)' % (', '.join(ips), row[1]))
 
for k in rules.keys():
    print '=== ' + k
    print " or\n".join(rules[k])
    print

