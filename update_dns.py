#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dns.resolver
from collections import OrderedDict
from app.models import DnsCache, Pool

custom_nameservers = ['8.8.8.8', '8.8.4.4']
my_resolver = dns.resolver.Resolver()
my_resolver.nameservers = custom_nameservers

def get_ips_for_domain(domain):
    """
    Returns a list of IPv4 addresses for the given domain.
    :param domain:
    :return:
    """
    results = my_resolver.query(domain, 'A')
    return [str(ip) for ip in results]


def retrieve_domains():
    """
    Returns the set of distinct domains from `pools.csv`.
    :return:
    """
    pools = Pool.read_pools('pools.csv', cached_only=False)
    return OrderedDict((x, True) for x in [p.domain for p in pools]).keys()


def update_dns():
    print("Retrieving DNS updates...")
    domains = retrieve_domains()
    for domain in domains:
        print(domain, end='')
        ips = ','.join(get_ips_for_domain(domain))
        dns = DnsCache(domain=domain, ips=ips)
        stored_dns = DnsCache.get_by_domain(domain)
        if stored_dns is None or stored_dns != dns:
            dns.save()
            print(' ... added', end='')
        print()


if __name__ == '__main__':
    update_dns()
