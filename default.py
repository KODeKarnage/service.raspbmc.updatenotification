# declare file encoding
# -*- coding: utf-8 -*-

#  Copyright (C) 2013 KodeKarnage
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html

import xbmcgui
import xbmcaddon
import xbmc
import os
import urllib2

__script_id__  = "service.raspbmc.updatenotification"
__addon__      = xbmcaddon.Addon(id=__script_id__)
__scriptPath__ = __addon__.getAddonInfo('path')
__image_file__ = os.path.join(__scriptPath__,'resources','media','RaspBMC_UA.png')


def log(vname, message):
	#if settings['debug']:
	xbmc.log(msg=vname + " -- " + str(message))


class Main():

    def __init__(self):
        self.window = xbmcgui.Window(10000)
        self.window.setProperty('RUA_notification','false')
        self.ex_version_sources =   [   "http://svn.stmlabs.com/svn/raspbmc/release/update-system/kernel/kver", 
                                        "http://svn.stmlabs.com/svn/raspbmc/release/update-system/xbmc-svcmgmt/svcver",
                                        "http://svn.stmlabs.com/svn/raspbmc/release/update-system/xbmc/xbmcver" ]
        self.in_version_sources =   [   "/scripts/upd_hist/kver",
                                        "/scripts/upd_hist/svcver",
                                        "/scripts/upd_hist/xbmcver" ] 
        self.check_ver()
        self.daemon()


    def _daemon(self):
        while not xbmc.abortRequested:
            available = __addon__.getSetting('Update_Available')
            notified = self.window.getProperty('RUA_notification')
            if available == 'true' and notified == 'false':
                #posts notification if update is available and notification is not currently displayed
                self.post_notification()
            elif available == 'false' and notified == 'true':
                #removes the notification if a check reveals there is no notification (should be needed, but just in case)
                self.takedown_notification()
            else:
                xbmc.sleep(10000)
                self.check_ver()


    def check_ver(self):
        for x in range(2):
            self.XV = urllib2.urlopen(self.ex_version_sources[x]).read()
            self.NV = os.popen(self.in_version_sources[x]).read()
            if self.XV != self.NV:
                __addon__.setSetting(id='Update_Available',value='true')
                break
            if x == 2:
                __addon__.setSetting(id='Update_Available',value='false')


    def post_notification(self):
        self.RUA_image = xbmcgui.ControlImage(15, 55, 150, 50, __image_file__)
        self.RUA_image.setVisibleCondition('!System.ScreenSaverActive')
        self.window.addControl(self.RUA_image)
        self.window.setProperty('RUA_notification','true')

    def takedown_notification(self):
        self.window.removeControl('RUA_image')
        self.window.setProperty('RUA_notification','false')

if __name__ == "__main__":
	Main()



          


