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

import re

from pywurfl.algorithms.wurfl import utils


# generic user agent normalizers

babel_fish_re = re.compile(ur"\s*\(via babelfish.yahoo.com\)\s*", re.UNICODE)
uplink_re = re.compile(ur"\s*UP\.Link.+$", re.UNICODE)
vodafone_re = re.compile(ur"/SN(\d+)\s", re.UNICODE)
yeswap_re = re.compile(ur"\s*Mozilla/4\.0 \(YesWAP mobile phone proxy\)",
                       re.UNICODE)
safari_re = re.compile(ur"(Mozilla\/5\.0.*)(\;\s*U\;.*?)(Safari\/\d{0,3})",
                       re.UNICODE)
ibm_wbi_re = re.compile(ur"\(via IBM WBI \d+\.\d+\)", re.UNICODE)
gmcc_re = re.compile(ur"GMCC/\d\.\d")


def babelfish(user_agent):
    """Replace the "via babelfish.yahoo.com" with ''"""
    #print "normalizer babelfish"
    return babel_fish_re.sub('', user_agent)


def blackberry(user_agent):
    """ Replaces the heading "BlackBerry" string with ''"""
    #print "normalizer blackberry"
    if u"BlackBerry" in user_agent and not user_agent.startswith(u"BlackBerry"):
        user_agent = user_agent[user_agent.index(u"BlackBerry"):]
    return user_agent


def uplink(user_agent):
    """Replace the trailing UP.Link ... with ''"""
    #print "normalizer uplink"
    return uplink_re.sub('', user_agent)


def vodafone(user_agent):
    """Normalize the "/SNnnnnnnnnnnnnnnnn" String."""
    #print "normalizer vodafone"
    match = vodafone_re.search(user_agent)
    if match:
        grp_repl = u"/SN" + "X" * (len(match.group()) - 4) + " "
        user_agent = vodafone_re.sub(grp_repl, user_agent)
    return user_agent


def yeswap(user_agent):
    """Replace the "YesWAP mobile phone proxy" with ''"""
    #print "normalizer yeswap"
    return yeswap_re.sub('', user_agent)


def ibm_wbi(user_agent):
    #print "normalizer ibm_wbi"
    return ibm_wbi_re.sub('', user_agent)


def gmcc(user_agent):
    #print "normalizer gmcc"
    return gmcc_re.sub('', user_agent)


def _combine_funcs(*funcs):
    def normalizer(user_agent):
        #print "applying default normalizer"
        for f in funcs:
            user_agent = f(user_agent)
        return user_agent.replace('  ', ' ').strip()
    return normalizer


default_normalizer = _combine_funcs(vodafone, blackberry, uplink, yeswap,
                                    babelfish, ibm_wbi, gmcc)


# specific user agent normalizers

def _specific_normalizer(user_agent, search_string, vsn_size):
    if search_string in user_agent:
        start = user_agent.index(search_string)
        user_agent = user_agent[start:start + vsn_size]
    return user_agent


def chrome(user_agent):
    #print "chrome normalizer"
    return _specific_normalizer(user_agent, u"Chrome", 8)


def firefox(user_agent):
    #print "firefox normalizer"
    return _specific_normalizer(user_agent, u"Firefox", 11)


def konqueror(user_agent):
    #print "konqueror normalizer"
    return _specific_normalizer(user_agent, u"Konqueror", 11)


def opera(user_agent):
    #print "opera normalizer"
    return _specific_normalizer(user_agent, u"Opera", 7)


def msie(user_agent):
    #print "msie normalizer"
    if u"MSIE" in user_agent:
        user_agent = user_agent[0:user_agent.index(u"MSIE")+9]
    return user_agent


def android(user_agent):
    #print "android normalizer"
    start = utils.ordinal_index(user_agent, ";", 3)
    end = utils.ordinal_index(user_agent, ";", 4)
    if start == -1 or end == -1:
        return user_agent
    return user_agent[:start] + user_agent[end:]


def safari(user_agent):
    """
    Return the safari user agent stripping out all the chararcters between
    U; and Safari/xxx

    e.g Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; fr) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.1 Safari/525.18
    becomes
    Mozilla/5.0 (Macintosh Safari/525
    """
    #print "safari normalizer"
    match = safari_re.search(user_agent)
    if match and len(match.groups()) >= 3:
        user_agent = " ".join([match.group(1).strip(), match.group(3).strip()])
    return user_agent

