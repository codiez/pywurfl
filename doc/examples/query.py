#!/usr/bin/env python

"""
pywurfl Query Language Example

Copyright 2006, Armand Lynch <lyncha@users.sourceforge.net>

This code is free software; you can redistribute it and/or modify it under
the terms of the LGPL License (see the file LICENSE included with the
distribution).
"""

from wurfl import devices
from pywurfl.ql import QL

q = QL(devices)
output = None

print '''
pywurfl Query Language Example v1.0
The pywurfl Query Language is very similiar to SQL.

Quick Language Overview
=======================

select (id|ua|device)
where capability operator value (and/or) (...)
where any(capability, capability, ...) operator value
where all(capability, capability, ...) operator value


Examples
========

"select id where ringtone=true"
"select ua where ringtone=true and any(ringtone_mp3, ringtone_aac)=false"

'''
print "Type 'output [filname]' to save your query and results"
print "Type 'q' or 'quit' alone to quit"
while 1:
    query = unicode(raw_input("query: ").strip())

    try:
        if query.startswith("output"):
            output = file(query.split()[1], "ab")
            print "Sending output to: %s" % output.name
            continue
    except (IOError, IndexError):
        print "Could not open file for writing"
        continue

    if query.strip().lower() == 'q' or query.strip().lower() == 'quit':
        break

    try:
        result = q(query)
        if output is not None:
            output.write(query + "\n\n")
        for x in result:
            print x
            if output is not None:
                output.write(x + "\n")
    except:
        print "I don't understand \"%s\"" % query
        continue

    if output is not None:
        output.write(x + "\n\n")
