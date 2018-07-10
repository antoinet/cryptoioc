#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import struct

def generate_sid(input):
    m = hashlib.sha1()
    m.update(input.encode('utf-8'))
    b = m.digest()
    num = struct.unpack('>i', b[0:4])
    return 9000000 + (num[0] % 1000000)