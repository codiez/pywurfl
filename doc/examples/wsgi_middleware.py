"""
pywurfl WSGI middleware example
See http://wsgi.org/wsgi for more information on WSGI

Copyright 2006, Armand Lynch <lyncha@users.sourceforge.net>

This code is free software; you can redistribute it and/or modify it under
the terms of the LGPL License (see the file LICENSE included with the
distribution).
"""

from pywurfl.algorithms import JaroWinkler
from pywurfl.exceptions import DeviceNotFound


class WURFLMiddleWare(object):
    def __init__(self, application, devices, search_algorithm):
        self.application = application
        self.devices = devices
        self.search_algorithm = search_algorithm

    def __call__(self, environ, start_response):
        try:
            device = self.devices.select_ua(environ['HTTP_USER_AGENT'],
                                            self.search_algorithm)
        except DeviceNotFound:
            device = devices.select_id(u'generic')
        environ['wurfl.device'] = device
        return self.application(environ, start_response)


def WURFLMiddleWareClosure(application, devices, search_algorithm):
    def middle_ware(environ, start_response):
        try:
            device = devices.select_ua(environ['HTTP_USER_AGENT'],
                                               search_algorithm)
        except DeviceNotFound:
            device = devices.select_id(u'generic')
        environ['wurfl.device'] = device
        return application(environ, start_response)
    return middle_ware

