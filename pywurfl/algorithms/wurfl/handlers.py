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
from pywurfl.algorithms.wurfl import normalizers
from pywurfl.algorithms.wurfl.strategies import ld_match, ris_match


uiol = utils.indexof_or_length
uoi = utils.ordinal_index


class AbstractMatcher(object):
    user_agent_map = {}

    def __init__(self, normalizer=None):
        if normalizer is None:
            self.normalizer = lambda x: x
        else:
            self.normalizer = normalizer
        self.known_user_agents = set()

    def add(self, user_agent, wurfl_id):
        self.known_user_agents.add(user_agent)
        self.user_agent_map[user_agent] = wurfl_id

    @property
    def user_agents(self):
        return sorted(self.known_user_agents)

    def can_handle(self, user_agent):
        raise NotImplementedError

    def __call__(self, user_agent):
        devid = self.conclusive_match(user_agent)
        if not devid or devid == u"generic":
            devid = self.recovery_match(user_agent)
        if not devid or devid == u"generic":
            devid = self.catch_all_recovery_match(user_agent)
        return devid

    def conclusive_match(self, user_agent):
        user_agent = self.normalizer(user_agent)
        match = self.look_for_matching_user_agent(user_agent)
        #print "%s -> conclusive_match -> %s" % (user_agent, match)
        devid = self.user_agent_map.get(match, u"generic")
        return devid

    def look_for_matching_user_agent(self, user_agent):
        tolerance = utils.first_slash(user_agent)
        #print "AbstractMatcher tolerance %s" % tolerance
        match = ris_match(self.user_agents, user_agent, tolerance)
        #print "AbstractMatcher %s -> l_f_m_ua -> %s" % (user_agent, match)
        return match

    def recovery_match(self, user_agent):
        return u"generic"

    recovery_map = (
        # Openwave
        (u"UP.Browser/7.2", u"opwv_v72_generic"),
        (u"UP.Browser/7", u"opwv_v7_generic"),
        (u"UP.Browser/6.2", u"opwv_v62_generic"),
        (u"UP.Browser/6", u"opwv_v6_generic"),
        (u"UP.Browser/5", u"upgui_generic"),
        (u"UP.Browser/4", u"uptext_generic"),
        (u"UP.Browser/3", u"uptext_generic"),

        # Series 60
        (u"Series60", u"nokia_generic_series60"),

        # Access/Net Front
        (u"NetFront/3.0", u"netfront_ver3"),
        (u"ACS-NF/3.0", u"netfront_ver3"),
        (u"NetFront/3.1", u"netfront_ver3_1"),
        (u"ACS-NF/3.1", u"netfront_ver3_1"),
        (u"NetFront/3.2", u"netfront_ver3_2"),
        (u"ACS-NF/3.2", u"netfront_ver3_2"),
        (u"NetFront/3.3", u"netfront_ver3_3"),
        (u"ACS-NF/3.3", u"netfront_ver3_3"),
        (u"NetFront/3.4", u"netfront_ver3_4"),
        (u"NetFront/3.5", u"netfront_ver3_5"),

        # Windows CE
        (u"Windows CE", u"ms_mobile_browser_ver1"),

        # web browsers?
        (u"Mozilla/4.0", u"generic_web_browser"),
        (u"Mozilla/5.0", u"generic_web_browser"),
        (u"Mozilla/5.0", u"generic_web_browser"),

        # Generic XHTML
        (u"Mozilla/", u"generic_xhtml"),
        (u"ObigoInternetBrowser/Q03C", u"generic_xhtml"),
        (u"AU-MIC/2", u"generic_xhtml"),
        (u"AU-MIC-", u"generic_xhtml"),
        (u"AU-OBIGO/", u"generic_xhtml"),
        (u"Obigo/Q03", u"generic_xhtml"),
        (u"Obigo/Q04", u"generic_xhtml"),
        (u"ObigoInternetBrowser/2", u"generic_xhtml"),
        (u"Teleca Q03B1", u"generic_xhtml"),

        # Opera Mini
        (u"Opera Mini/1", u"opera_mini_ver1"),
        (u"Opera Mini/2", u"opera_mini_ver2"),
        (u"Opera Mini/3", u"opera_mini_ver3"),
        (u"Opera Mini/4", u"opera_mini_ver4"),

        # DoCoMo
        (u"DoCoMo", u"docomo_generic_jap_ver1"),
        (u"KDDI", u"docomo_generic_jap_ver1"))

    def catch_all_recovery_match(self, user_agent):

        match = u"generic"
        for partial_agent, wdevice in self.recovery_map:
            if partial_agent in user_agent:
                match = wdevice
                break
        return match


class AlcatelMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return (user_agent.startswith(u"Alcatel") or
                user_agent.startswith(u"ALCATEL"))


class AndroidMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return u"Android" in user_agent

    def look_for_matching_user_agent(self, user_agent):
        tolerance = uiol(user_agent, u" ",
                         start_index=uiol(user_agent, u"Android"))
        match = ris_match(self.user_agents, user_agent, tolerance)
        #print "AndroidMatcher %s -> l_f_m_ua -> %s" % (user_agent, match)
        return match

    def recovery_match(self, user_agent):
        return u"generic_android"


class AOLMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return not utils.is_mobile_browser(user_agent) and u"AOL" in user_agent


class AppleMatcher(AbstractMatcher):
    APPLE_LD_TOLERANCE = 5

    def can_handle(self, user_agent):
        return (u"iPhone" in user_agent or u"iPod" in user_agent or u"iPad" in
                user_agent)

    def look_for_matching_user_agent(self, user_agent):
        tolerance = utils.first_semi_colon(user_agent)
        match = ld_match(self.user_agents, user_agent, tolerance)
        #print "AppleMatcher %s -> l_f_m_ua -> %s" % (user_agent, match)
        return match

    def recovery_match(self, user_agent):
        if u"iPad" in user_agent:
            return "apple_ipad_ver1"
        if u"iPod" in user_agent:
            return u"apple_ipod_ver1"
        return u"apple_iphone_ver1"


class BenQMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return user_agent.startswith(u"BENQ") or user_agent.startswith(u"BenQ")


class BlackberryMatcher(AbstractMatcher):
    blackberries = {}
    blackberries["2."] = u"blackberry_generic_ver2"
    blackberries["3.2"] = u"blackberry_generic_ver3_sub2"
    blackberries["3.3"] = u"blackberry_generic_ver3_sub30"
    blackberries["3.5"] = u"blackberry_generic_ver3_sub50"
    blackberries["3.6"] = u"blackberry_generic_ver3_sub60"
    blackberries["3.7"] = u"blackberry_generic_ver3_sub70"
    blackberries["4."] = u"blackberry_generic_ver4"

    def can_handle(self, user_agent):
        return u"BlackBerry" in user_agent

    def recovery_match(self, user_agent):
        match = u"generic"

        if user_agent.startswith(u"BlackBerry"):
            version = self.get_version(user_agent)
            match = self.blackberries.get(version, u"generic")

        return match

    def get_version(self, user_agent):
        version = u""
        position = user_agent.index('/')
        if position + 4 < len(user_agent):
            version = user_agent[position+1:position+4]
        return version


class BotMatcher(AbstractMatcher):
    bots = (u"bot", u"crawler", u"spider", u"novarra", u"transcoder",
            u"yahoo! searchmonkey", u"yahoo! slurp", u"feedfetcher-google",
            u"toolbar", u"mowser")

    BOT_TOLERANCE = 4

    def can_handle(self, user_agent):
        user_agent = user_agent.lower()
        for bot in self.bots:
            if bot in user_agent:
                return True
        return False

    def look_for_matching_user_agent(self, user_agent):
        match = ld_match(self.user_agents, user_agent, self.BOT_TOLERANCE)
        return match

    def recovery_match(self, user_agent):
        return u"generic_web_crawler"


class CatchAllMatcher(AbstractMatcher):
    MOZILLA_LD_TOLERANCE = 4

    def can_handle(self, user_agent):
        return True

    def look_for_matching_user_agent(self, user_agent):
        if user_agent.startswith(u"Mozilla"):
            if user_agent.startswith(u"Mozilla/4"):
                match = ld_match(self.extract_uas(u"Mozilla/4"), user_agent,
                                 self.MOZILLA_LD_TOLERANCE)
            elif user_agent.startswith(u"Mozilla/5"):
                match = ld_match(self.extract_uas(u"Mozilla/5"), user_agent,
                                 self.MOZILLA_LD_TOLERANCE)
            else:
                match = ld_match(self.extract_uas(u"Mozilla"), user_agent,
                                 self.MOZILLA_LD_TOLERANCE)
        else:
            match = AbstractMatcher.look_for_matching_user_agent(self,
                                                                 user_agent)
        #print "CatchAllMatcher %s -> l_f_m_ua -> %s" % (user_agent, match)
        return match

    def extract_uas(self, start):
        return (x for x in self.user_agents if x.startswith(start))


class ChromeMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return (not utils.is_mobile_browser(user_agent) and
                u"Chrome" in user_agent)


class DoCoMoMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return user_agent.startswith(u"DoCoMo")

    def look_for_matching_user_agent(self, user_agent):
        return u""

    def recovery_match(self, user_agent):
        if user_agent.startswith(u"DoCoMo/2"):
            return u"docomo_generic_jap_ver2"
        return u"docomo_generic_jap_ver1"


class FirefoxMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return (not utils.is_mobile_browser(user_agent) and
                u"Firefox" in user_agent)


class GrundigMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return (user_agent.startswith(u"Grundig") or
                user_agent.startswith(u"GRUNDIG"))


class HTCMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return user_agent.startswith(u"HTC")


class KDDIMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return u"KDDI" in user_agent

    def look_for_matching_user_agent(self, user_agent):
        if user_agent.startswith(u"KDDI/"):
            tolerance = utils.second_slash(user_agent)
        elif user_agent.startswith(u"KDDI"):
            tolerance = utils.first_slash(user_agent)
        else:
            tolerance = uiol(user_agent, ")")

        match = ris_match(self.user_agents, user_agent, tolerance)
        #print "KDDIMatcher %s -> l_f_m_ua -> %s" % (user_agent, match)
        return match

    def recovery_match(self, user_agent):
        if u"Opera" in user_agent:
            return u"opera"
        return u"opwv_v62_generic"


class KonquerorMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return (not utils.is_mobile_browser(user_agent) and
                u"Konqueror" in user_agent)


class KyoceraMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return (user_agent.startswith(u"kyocera") or
                user_agent.startswith(u"QC-") or
                user_agent.startswith(u"KWC-"))


class LGMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return (user_agent.startswith(u"lg") or u"LG-" in user_agent or
                u"LGE" in user_agent)

    def look_for_matching_user_agent(self, user_agent):
        if u"Vodafone" in user_agent:
            tolerance = uiol(user_agent, u"LG")
        elif user_agent.startswith(u"LGE/") or user_agent.startswith("LG/"):
            tolerance = utils.second_slash(user_agent)
        else:
            tolerance = utils.first_slash(user_agent)

        return ris_match(self.user_agents, user_agent, tolerance)


class MitsubishiMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return user_agent.startswith(u"Mitsu")


class MotorolaMatcher(AbstractMatcher):
    MOTOROLA_TOLERANCE = 5

    def can_handle(self, user_agent):
        return (user_agent.startswith(u"Mot-") or
                u"MOT-" in user_agent or
                u"Motorola" in user_agent)

    def look_for_matching_user_agent(self, user_agent):
        if (user_agent.startswith(u"Mot-") or user_agent.startswith(u"MOT-") or
            user_agent.startswith(u"Motorola")):
            match = AbstractMatcher.look_for_matching_user_agent(self,
                                                                 user_agent)
        else:
            match = ld_match(self.user_agents, user_agent,
                             self.MOTOROLA_TOLERANCE)
        #print "MotorolaMatcher %s -> l_f_m_ua -> %s" % (user_agent, match)
        return match

    def recovery_match(self, user_agent):
        if u"MIB/2.2" in user_agent or u"MIB/BER2.2" in user_agent:
            match = u"mot_mib22_generic"
        else:
            match = u"generic"
        return match


class MSIEMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return (not utils.is_mobile_browser(user_agent) and
                user_agent.startswith(u"Mozilla") and
                u"MSIE" in user_agent)


class NecMatcher(AbstractMatcher):

    NEC_LD_TOLERANCE = 2

    def can_handle(self, user_agent):
        return user_agent.startswith(u"NEC") or user_agent.startswith(u"KGT")

    def look_for_matching_user_agent(self, user_agent):
        if user_agent.startswith(u"NEC"):
            match = AbstractMatcher.look_for_matching_user_agent(self,
                                                                 user_agent)
        else:
            match = ld_match(self.user_agents, user_agent,
                             self.NEC_LD_TOLERANCE)
        #print "NecMatcher %s -> l_f_m_ua -> %s" % (user_agent, match)
        return match


class NokiaMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return u"Nokia" in user_agent

    def look_for_matching_user_agent(self, user_agent):
        tolerance = uiol(user_agent, u"/",
                         start_index=user_agent.index(u"Nokia"))
        #print "NokiaMatcher tolerance %s" % tolerance
        match = ris_match(self.user_agents, user_agent, tolerance)
        #print "NokiaMatcher %s -> l_f_m_ua -> %s" % (user_agent, match)
        return match

    def recovery_match(self, user_agent):
        if u"Series60" in user_agent:
            match = u"nokia_generic_series60"
        elif u"Series80" in user_agent:
            match = u"nokia_generic_series80"
        else:
            match = u"generic"
        return match


class OperaMatcher(AbstractMatcher):

    OPERA_TOLERANCE = 3

    operas = {}
    operas["7"] = u"opera_7"
    operas["8"] = u"opera_8"
    operas["9"] = u"opera_9"
    operas["10"] = u"opera_10"

    opera_re = re.compile(r".*Opera/(\d+).*")

    def can_handle(self, user_agent):
        return (not utils.is_mobile_browser(user_agent) and
                u"Opera" in user_agent)

    def look_for_matching_user_agent(self, user_agent):
        match = ld_match(self.user_agents, user_agent, self.OPERA_TOLERANCE)
        #print "OperaMatcher %s -> l_f_m_ua -> %s" % (user_agent, match)
        return match

    def recovery_match(self, user_agent):
        match = self.opera_re.match(user_agent)
        if match:
            return self.operas.get(match.groups()[0], u"opera")
        return u"opera"


class OperaMiniMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return u"Opera Mini" in user_agent

    def recovery_match(self, user_agent):
        match = u""
        if u"Opera Mini/1" in user_agent:
            match = u"opera_mini_ver1"
        elif u"Opera Mini/2" in user_agent:
            match = u"opera_mini_ver2"
        elif u"Opera Mini/3" in user_agent:
            match = u"opera_mini_ver3"
        elif u"Opera Mini/4" in user_agent:
            match = u"opera_mini_ver4"
        return match


class PanasonicMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return user_agent.startswith(u"Panasonic")


class PantechMatcher(AbstractMatcher):

    PANTECH_LD_TOLERANCE = 4

    def can_handle(self, user_agent):
        return (user_agent.startswith(u"Pantech") or
                user_agent.startswith(u"PT-") or
                user_agent.startswith(u"PANTECH") or
                user_agent.startswith(u"PG-"))

    def look_for_matching_user_agent(self, user_agent):
        if user_agent.startswith(u"Pantech"):
            match = ld_match(self.user_agents, user_agent,
                             self.PANTECH_LD_TOLERANCE)
        else:
            match = AbstractMatcher.look_for_matching_user_agent(self,
                                                                 user_agent)
        #print "PantechMatcher %s -> l_f_m_ua -> %s" % (user_agent, match)
        return match


class PhilipsMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return (user_agent.startswith(u"Philips") or
                user_agent.startswith(u"PHILIPS"))


class PortalmmmMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return user_agent.startswith(u"portalmmm")

    def look_for_matching_user_agent(self, user_agent):
        return u""


class QtekMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return user_agent.startswith(u"Qtek")


class SafariMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return (not utils.is_mobile_browser(user_agent) and
                user_agent.startswith(u"Mozilla") and
                u"Safari" in user_agent)

    def recovery_match(self, user_agent):
        if u"Macintosh" in user_agent or u"Windows" in user_agent:
            match =  u"generic_web_browser"
        else:
            match = u"generic"
        return match


class SagemMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return (user_agent.startswith(u"Sagem") or
                user_agent.startswith(u"SAGEM"))


class SamsungMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return (u"Samsung/SGH" in user_agent or
                user_agent.startswith(u"SEC-") or
                user_agent.startswith(u"Samsung") or
                user_agent.startswith(u"SAMSUNG") or
                user_agent.startswith(u"SPH") or
                user_agent.startswith(u"SGH") or
                user_agent.startswith(u"SCH"))

    def look_for_matching_user_agent(self, user_agent):
        if (user_agent.startswith(u"SEC-") or
            user_agent.startswith(u"SAMSUNG-") or
            user_agent.startswith(u"SCH")):
            tolerance = utils.first_slash(user_agent)
        elif (user_agent.startswith(u"Samsung") or
              user_agent.startswith(u"SPH") or
              user_agent.startswith(u"SGH")):
            tolerance = utils.first_space(user_agent)
        elif user_agent.startswith(u"SAMSUNG/"):
            tolerance = utils.second_slash(user_agent)
        elif u"Samsung/SGH-L870" in user_agent:
            tolerance = uiol(user_agent, u"/", 5)
        else:
            tolerance = len(user_agent)
        match = ris_match(self.user_agents, user_agent, tolerance)
        #print "SamsungMatcher %s -> l_f_m_ua -> %s" % (user_agent, match)
        return match


class SanyoMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return (user_agent.startswith(u"Sanyo") or
                user_agent.startswith(u"SANYO"))


class SharpMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return (user_agent.startswith(u"Sharp") or
                user_agent.startswith(u"SHARP"))


class SiemensMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return user_agent.startswith(u"SIE-")


class SonyEricssonMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return u"SonyEricsson" in user_agent

    def look_for_matching_user_agent(self, user_agent):
        if user_agent.startswith(u"SonyEricsson"):
            match = AbstractMatcher.look_for_matching_user_agent(self,
                                                                 user_agent)
        else:
            tolerance = utils.second_slash(user_agent)
            match = ris_match(self.user_agents, user_agent, tolerance)
        #print "SonyEricssonMatcher %s -> l_f_m_ua -> %s" % (user_agent, match)
        return match


class SPVMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return u"SPV" in user_agent

    def look_for_matching_user_agent(self, user_agent):
        tolerance = uiol(user_agent, u";", start_index=uiol(user_agent, u"SPV"))
        match = ris_match(self.user_agents, user_agent, tolerance)
        return match


class ToshibaMatcher(AbstractMatcher):
    def can_handle(self, user_agent):
        return user_agent.startswith(u"Toshiba")


class VodafoneMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith(u"Vodafone")

    def look_for_matching_user_agent(self, user_agent):
        tolerance = uiol(user_agent, u"/", 3)
        match = ris_match(self.user_agents, user_agent, tolerance)
        #print "VodafoneMatcher %s -> l_f_m_ua -> %s" % (user_agent, match)
        return match


class WindowsCEMatcher(AbstractMatcher):
    WINDOWS_CE_TOLERANCE = 3

    def can_handle(self, user_agent):
        return u"Mozilla/" in user_agent and (u"Windows CE" in user_agent or
                                              u"WindowsCE" in user_agent)

    def look_for_matching_user_agent(self, user_agent):
        match = ld_match(self.user_agents, user_agent,
                         self.WINDOWS_CE_TOLERANCE)
        return match

    def recovery_match(self, user_agent):
        return u"ms_mobile_browser_ver1"


handlers = [NokiaMatcher(),
            AndroidMatcher(normalizers.android),
            SonyEricssonMatcher(),
            MotorolaMatcher(),
            BlackberryMatcher(),
            SiemensMatcher(),
            SagemMatcher(),
            SamsungMatcher(),
            PanasonicMatcher(),
            NecMatcher(),
            QtekMatcher(),
            MitsubishiMatcher(),
            PhilipsMatcher(),
            LGMatcher(),
            AppleMatcher(),
            KyoceraMatcher(),
            AlcatelMatcher(),
            SharpMatcher(),
            SanyoMatcher(),
            BenQMatcher(),
            PantechMatcher(),
            ToshibaMatcher(),
            GrundigMatcher(),
            HTCMatcher(),
            BotMatcher(),
            SPVMatcher(),
            WindowsCEMatcher(),
            PortalmmmMatcher(),
            DoCoMoMatcher(),
            KDDIMatcher(),
            VodafoneMatcher(),
            OperaMiniMatcher(),
            ChromeMatcher(normalizers.chrome),
            AOLMatcher(),
            OperaMatcher(normalizers.opera),
            KonquerorMatcher(normalizers.konqueror),
            SafariMatcher(normalizers.safari),
            FirefoxMatcher(normalizers.firefox),
            MSIEMatcher(normalizers.msie),
            CatchAllMatcher()]

