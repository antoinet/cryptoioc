#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from app import app, db
from sqlalchemy import desc
from ipaddress import IPv4Address
from datetime import datetime


class DnsCache(db.Model):
    """
    ORM mapped model for a DNS cache.
    """
    domain = db.Column(db.String(128), primary_key=True, nullable=False)
    __ips = db.Column('ips', db.String(256))
    timestamp = db.Column(db.DateTime, primary_key=True, nullable=False)

    def __repr__(self):
        return '<DnsCache %r>' % self.domain

    def __eq__(self, other):
        return self.domain == other.domain and self.ips == other.ips

    def __str__(self):
        return "%s (%s) %s" % (self.domain, self.ips, self.timestamp.strftime('%Y-%m-%d %H:%M:%s'))

    @property
    def ips(self):
        return self.__ips

    @ips.setter
    def ips(self, ips):
        self.__ips = DnsCache.normalize_ips(ips)

    def save(self):
        """
        Persist the user in the database.
        :return:
        """
        self.timestamp = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def normalize_ips(ips):
        """
        Returns a sorted list of IP addresses.
        :param ips:
        :return:
        """
        l1 = sorted([IPv4Address(x.strip()) for x in ips.split(',')])
        return ','.join(map(str, l1))

    @staticmethod
    def get_by_domain(domain):
        """
        Returns the latest (youngest) DNS cache entry for the given domain.
        :param domain:
        :return:
        """
        return DnsCache.query\
            .filter(DnsCache.domain == domain)\
            .order_by(desc(DnsCache.timestamp))\
            .first()


class Pool(object):
    """
    Represents Mining Pool objects.
    """
    def __init__(self, domain, port, currency, comment=None):
        self.domain = domain
        self.port = port
        self.currency = currency
        self.comment = comment
        self.dns_cache = DnsCache.get_by_domain(domain)


    @staticmethod
    def read_pools(filename, cached_only=True):
        pools = []
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                domain, port, currency, comment = row
                pools.append(Pool(domain, port, currency, comment))
        if cached_only:
            return [x for x in pools if x.dns_cache]
        else:
            return pools
