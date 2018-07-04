#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app, db

class Ioc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(128), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(16))
    comment = db.Column(db.String(128))

    def __repr__(self):
        return '<Ioc %r>' % self.domain

class Ip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(128), nullable=False)
    ioc_id = db.Column(db.Integer, db.ForeignKey('ioc.id'), nullable=False)
    ioc = db.relationship('Ioc', backref=db.backref('ips', lazy=True))

    def __repr__(self):
        return '<Ip %r>' % self.ip
