# pywurfl - Wireless Universal Resource File Tools in Python
# Copyright (C) 2006-2010 Armand Lynch
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# Armand Lynch <lyncha@users.sourceforge.net>

__doc__ = """
This module contains the supporting classes for the Two Step Analysis user agent
algorithm that is used as the primary way to match user agents with the Java API
for the WURFL.

A description of the way the following source is intended to work can be found
within the source for the original Java API implementation here:
http://sourceforge.net/projects/wurfl/files/WURFL Java API/

The original Java code is GPLd and Copyright (c) 2008-2009 WURFL-Pro srl
"""

__author__ = "Armand Lynch <lyncha@users.sourceforge.net>"
__copyright__ = "Copyright 2010, Armand Lynch"
__license__ = "LGPL"
__url__ = "http://celljam.net/"
__version__ = "1.0.1"

from functools import partial


def is_mobile_browser(user_agent):
    user_agent = user_agent.lower()
    mobile_browsers = [u"tablet", u"mobile", u"wireless", u"palm", u"blazer",
                       u"netfront", u"symbian", u"bolt", u"iris", u"pocketpc"]
    for mb in mobile_browsers:
        if mb in user_agent:
            return True
    return False


def ordinal_index(target, needle=u" ", ordinal=1, start_index=0):
    index = -1

    working_target = target[start_index+1:]

    if needle in working_target:
        i = 0
        for i, x in enumerate(working_target.split(needle)):
            if ordinal < 1:
                break
            index += len(x)
            ordinal -= 1
        index += (i * len(needle)) + start_index + 1
        index = index - (len(needle) - 1)
    if ordinal != 0:
        index = -1
    return index


def find_or_length(func, user_agent):
    value = func(user_agent)
    if value == -1:
        value = len(user_agent)
    return value


def indexof_or_length(target, needle=u" ", position=1, start_index=0):
    value = ordinal_index(target, needle, position, start_index)
    if value == -1:
        value = len(target)
    return value


first_space = indexof_or_length
first_slash = partial(indexof_or_length, needle=u"/")
second_slash = partial(indexof_or_length, needle=u"/", position=2)
first_semi_colon = partial(indexof_or_length, needle=u";")


