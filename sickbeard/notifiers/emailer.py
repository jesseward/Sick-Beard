# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sick Beard.  If not, see <http://www.gnu.org/licenses/>.

import smtplib
from smtplib import SMTPException

import sickbeard
from sickbeard import logger, common
from sickbeard.exceptions import ex

class EMAILNotifier:
    """ Adds simple email notification to SickBeard """

    def notify_snatch(self, ep_name):
        if sickbeard.EMAIL_NOTIFY_ONSNATCH:
            self._notifyEMAIL(ep_name, "Snatch")

    def notify_download(self, ep_name):
        if sickbeard.EMAIL_NOTIFY_ONDOWNLOAD:
            self._notifyEMAIL(ep_name, "Download")

    def test_notify(self):
        return self._notifyEMAIL("test-episode", "test-message", \
                     "Testing SickBeard email notifications.")

    def _to_addr(self):
        return sickbeard.EMAIL_TO_ADDR

    def _from_addr(self):
        return sickbeard.EMAIL_FROM_ADDR

    def _mta_host(self):
        return sickbeard.EMAIL_MTA_HOST

    def _mta_port(self):
        return sickbeard.EMAIL_MTA_PORT

    def _notifyEMAIL(self, ep_name, sbtype, subject=None):

        if not self._mta_port  or not self._mta_host:
            logger.log(u"Mail server name or port not specified, skipping", logger.DEBUG)
            return False

        if not self._to_addr or not self._from_addr:
            logger.log(u"To: or From: fields not specified, skipping", \
                            logger.DEBUG)
            return False 

        if not subject:
            subject = "[SickBeard] %s of '%s' complete." % \
                        (sbtype, ep_name)
        
        message = ("To: %s\nFrom: %s\nSubject: %s\n\n"  \
                   "Alert : completed a %s of %s" \
                     % (self._to_addr, \
                        self._from_addr, \
                        subject, \
                        sbtype, \
                        ep_name))

        try:
            s = smtplib.SMTP(self._mta_host, self._mta_port)
            s.sendmail(self._from_addr, self._to_addr, message)
        except SMTPException:
            logger.log(u"Error sendmail message, please check settings", \
                        logger.ERROR)
            return False
            
        logger.log(u"Sent email notification", logger.DEBUG)

        return True

notifier = EMAILNotifier
