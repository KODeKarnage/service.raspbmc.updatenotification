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
import random
import datetime

__script_id__  = "service.raspbmc.updatenotification"
__addon__      = xbmcaddon.Addon(id=__script_id__)
__scriptPath__ = __addon__.getAddonInfo('path')
__image_file__ = os.path.join(__scriptPath__,'resources','media','RaspBMC_UA.png')
__addon__.setSetting(id='Update_Available',value='false')

def log(label, message):
    #if settings['debug']:
    xbmc.log(msg='RaspBMC_Notify: ' + str(label) + ' - ' + str(message))


class Main():

    def __init__(self):
        xbmc.sleep(60000)
        self.window = xbmcgui.Window(10000)
        self.window.setProperty('RUA_notification','false')
        self.ex_version_sources =   [   "http://svn.stmlabs.com/svn/raspbmc/release/update-system/kernel/kver", 
                                        "http://svn.stmlabs.com/svn/raspbmc/release/update-system/xbmc-svcmgmt/svcver",
                                        "http://svn.stmlabs.com/svn/raspbmc/release/update-system/xbmc/xbmcver" ]
        self.in_version_sources =   [   "/scripts/upd_hist/kver",
                                        "/scripts/upd_hist/svcver",
                                        "/scripts/upd_hist/xbmcver" ] 
        self.base_time    = datetime.datetime.now()
        self.recheck_time = datetime.datetime.now()
        self.first_run    = True
        self.check_ver()
        self._daemon()


    def _daemon(self):
        while not xbmc.abortRequested:
            
            self.current_time = datetime.datetime.now()

            if self.recheck_time < self.current_time or self.first_run == True:

                self.first_run = False
                self.randy = (float(random.randint(750,1250))/1000.0)*86400.0
                self.recheck_time = self.recheck_time + datetime.timedelta(seconds=self.randy)
                log('recheck time',self.recheck_time)
                
                available = __addon__.getSetting('Update_Available')
                notified = self.window.getProperty('RUA_notification')
                log('available',available)
                log('notified',notified)

                if available == 'true' and notified == 'false':
                    #posts notification if update is available and notification is not currently displayed
                    self.post_notification()
                elif available == 'false' and notified == 'true':
                    #removes the notification if a check reveals there is no notification (should be needed, but just in case)
                    self.takedown_notification()
                else:
                    self.check_ver()
            xbmc.sleep(2500)    
        self.takedown_notification()


    def check_ver(self):
        for x in range(2):
            self.XV = urllib2.urlopen(self.ex_version_sources[x]).read()
            log('url_read',self.XV)
            with open(self.in_version_sources[x],'r') as f:
                self.NV = f.read()
            log('local_read',self.NV)
            if self.XV > self.NV:
                __addon__.setSetting(id='Update_Available',value='true')

                break
            if x == 2:
                __addon__.setSetting(id='Update_Available',value='false')


    def post_notification(self):
        log('notifying','posting notification')
        self.RUA_image = xbmcgui.ControlImage(15, 55, 150, 50, __image_file__)
        self.window.addControl(self.RUA_image)
        self.window.setProperty('RUA_notification','true')
        self.RUA_image.setVisibleCondition('!System.ScreenSaverActive')

    def takedown_notification(self):
        self.window.removeControl(self.RUA_image)
        self.window.setProperty('RUA_notification','false')

if __name__ == "__main__":
    srv = Main()
    del srv
