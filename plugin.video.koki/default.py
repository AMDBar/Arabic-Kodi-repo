# -*- coding: utf-8 -*-

'''
    koki Add-on
    Copyright (C) 2016 Dr Tharwat

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
 
import requests, util
import urlresolver
import xbmcaddon, xbmcgui
import urllib
import sys


my_addon = xbmcaddon.Addon()
my_setting = my_addon.getSetting('koki_setting') # returns the string 'true' or 'false'
my_addon.setSetting('koki_setting', 'true')


def playVideo(params): 

    web_url = (params['videolink'])
    media_url = urlresolver.resolve(web_url) 
    stream_link = str(media_url) 
    print "stream_link",stream_link 
    if stream_link is None: 
        return 'no stream found'
    
     
    
    util.playMedia(params['title'], params['image'], stream_link, 'Video')
    
def menuLink(params):  
    caption = 'try HD first: #1--OK.ru ,#2--openload(try it several clicks until work) '
    action = {'info':1}
    cap_link = util.makeLink(action)
    util.addMenuItem(caption, cap_link, icon, fanart, False)
    url = (params['video'])
    videoPage = requests.get(url)
    if videoPage and videoPage.status_code == 200:
        cont = videoPage.text
        vidlinks = util.extractAll(cont, '<div id="tab', '/div>')

        for vidlink in vidlinks:
            t = util.extract(vidlink,'://','/')
            v = util.extract(vidlink,'SRC="','"') or util.extract(vidlink,'src="','"')
            paramz= {'play':1}
            paramz['title'] = t
            paramz['videolink'] = v
            paramz['image'] = params['image']
            link = util.makeLink(paramz)
            
            util.addMenuItem(paramz['title'], link, 'DefaultVideo.png', paramz['image'], False)
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to create menu' % (url))
    util.endListing()

def ololink(params):
    caption = 'If you have trouble:goto:https://sites.google.com/site/kokiarbic/help'
    action = {'info':1}
    cap_link = util.makeLink(action)
    util.addMenuItem(caption, cap_link, icon, fanart, False)
    url = (params['video'])
    videoPage = requests.get(url)
    if videoPage and videoPage.status_code == 200:
        cont = videoPage.text
        vidlinks = util.extractAll(cont, '"playerst"', '/iframe>')
        for vidlink in vidlinks:
            t = 'Movielink'
            v = util.extract(vidlink,'SRC="','"') or util.extract(vidlink,'src="','"')
            paramz= {'play':1}
            paramz['title'] = t
            paramz['videolink'] = v
            paramz['image'] = params['image']
            link = util.makeLink(paramz)
            util.addMenuItem(paramz['title'], link, 'DefaultVideo.png', paramz['image'], False)
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to create menu' % (url))
    util.endListing()

def pages(params):
    page = int(params['page'])
    p = 'page:' + str(page)
    util.addMenuItem(p, None, None, None, False)

    Baseurl = 'http://el7l.tv/online2/12/_%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9/'
    url = Baseurl + '%d.html' % (page)
    response = requests.get(url)
    if response and response.status_code == 200:
        cont = response.text
        videos = util.extractAll(cont, '<div class="file_index">', '/div>')
        for video in videos:
            t = util.extract(video,'alt="','"')
            v = util.extract(video,'a href="http://el7l.tv/online','"')
            vp = 'http://el7l.tv/play'+ v
            i = util.extract(video,'img src="','"')
            params={'listing':1}
            params['title']= t
            params['video']= vp
            params['image']= i
            link = util.makeLink(params)
            util.addMenuItem(params['title'], link, 'DefaultVideo.png', params['image'], True)
        
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to create menu' % (url))
    
    parms = {'old':1,'page':str(page + 1)}
    page_link = util.makeLink(parms)
    util.addMenuItem('Next Page:>> ', page_link, None, None, True)
    util.endListing()

def buildMenu():
    url = 'http://el7l.tv/online2/12/_%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9/1.html'
    response = requests.get(url)
    if response and response.status_code == 200:
        cont = response.text
        videos = util.extractAll(cont, '<div class="file_index">', '/div>')
        for video in videos:
            t = util.extract(video,'alt="','"')
            v = util.extract(video,'a href="http://el7l.tv/online','"')
            vp = 'http://el7l.tv/play'+ v
            i = util.extract(video,'img src="','"')
            params={'listing':1}
            params['title']= t
            params['video']= vp
            params['image']= i
            link = util.makeLink(params)
            util.addMenuItem(params['title'], link, 'DefaultVideo.png', params['image'], True)
                           
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to create menu' % (url))

    pages = {'page':1}
    page_link = util.makeLink(pages)
    util.addMenuItem('Next Page:>> ', page_link, None, None, True)
    util.endListing() 

def old(params):
    page = int(params['page'])
    p = 'page:' + str(page)
    util.addMenuItem(p, None, None, None, False)

    Baseurl = 'http://el7l.tv/online2/400/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%A7%D8%A8%D9%8A%D8%B6_%D9%88%D8%A7%D8%B3%D9%88%D8%AF/'
    url = Baseurl + '%d.html' % (page)
    response = requests.get(url)
    if response and response.status_code == 200:
        cont = response.text
        videos = util.extractAll(cont, '<div class="file_index">', '/div>')
        for video in videos:
            t = util.extract(video,'alt="','"')
            v = util.extract(video,'a href="http://el7l.tv/online','"')
            vp = 'http://el7l.tv/play'+ v
            i = util.extract(video,'img src="','"')
            params={'olo':1}
            params['title']= t
            params['video']= vp
            params['image']= i
            link = util.makeLink(params)
            util.addMenuItem(params['title'], link, 'DefaultVideo.png', params['image'], True)
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to create menu' % (url))
    parms = {'old':1,'page':str(page + 1)}
    page_link = util.makeLink(parms)
    util.addMenuItem('Next Page:>> ', page_link, None, None, True)
    util.endListing()

def special(params):
    page = int(params['page'])
    p = 'page:' + str(page)
    util.addMenuItem(p, None, None, None, False) % (page)


    Baseurl = 'http://el7l.tv/online2/13/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9_%D9%84%D9%84%D9%83%D8%A8%D8%A7%D8%B1_%D9%81%D9%82%D8%B7/'
    url = Baseurl + '%d.html' % (page)
    response = requests.get(url)
    if response and response.status_code == 200:
        cont = response.text
        videos = util.extractAll(cont, '<div class="file_index">', '/div>')
        for video in videos:
            t = util.extract(video,'alt="','"')
            v = util.extract(video,'a href="http://el7l.tv/online','"')
            vp = 'http://el7l.tv/play'+ v
            i = util.extract(video,'img src="','"')
            params={'listing':1}
            params['title']= t
            params['video']= vp
            params['image']= i
            link = util.makeLink(params)
            util.addMenuItem(params['title'], link, 'DefaultVideo.png', params['image'], True)
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to create menu' % (url))
    
    parms = {'spec':1,'page':str(page + 1)}
    page_link = util.makeLink(parms)
    util.addMenuItem('Next Page:>> ', page_link, None, None, True)
    util.endListing()

def searchp(params):
    url = (params['url'])
    videoPage = requests.get(url)
    if videoPage and videoPage.status_code == 200:
        cont = videoPage.text
        vidlinks = util.extractAll(cont, '<div id="tab', '/div>')
        for vidlink in vidlinks:
            t = util.extract(vidlink, '://', '/')
            v = util.extract(vidlink, 'SRC="', '"') or util.extract(vidlink, 'src="', '"')
            paramz = {'play':1}
            paramz['title'] = t
            paramz['videolink'] = v
            paramz['image'] = icon
            link = util.makeLink(paramz)
            util.addMenuItem(paramz['title'], link, paramz['image'], None, False)
        util.endListing()
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to create menu' % (url))

def search():
    dialog = xbmcgui.Dialog()
    i = dialog.input('Enter Movie Name:', type=xbmcgui.INPUT_ALPHANUM)
    q= urllib.quote(i, safe="%/:=&?~#+!$,;'@()*[]")
    baseurl = 'https://www.google.com.sa/search?rlz=1C1CHZL_enSA679SA679&espv=2&q=el7al.tv+'
    print q
    url = baseurl + q +'&oq=el7al.tv+'+ q +'&gs_l=serp.3...33231.51533.0.52317.42.30.8.0.0.0.211.4360.0j21j4.25.0....0...1c.1.64.serp..11.22.2813.0..0j30i10k1j0i13k1j0i13i30k1j0i7i30k1j35i39k1j0i131k1j0i10i30k1j0i13i10k1.w4AW4pCV-E4'
    response = requests.get(url)
    if response and response.status_code == 200:
        cont = response.text
        videos = util.extractAll(cont, '<a href="/url?q=http://el7l.tv/online', 'class="_cD"')
        for video in videos:
            t = util.extract(video, '>', '</a>')
            t1 = (t.replace('\n', '').replace('\t', '').replace('</b>', '').replace('<b>', '').lstrip())
            u1 = (util.extract(video, '/', '&'))
            u = 'http://el7l.tv/play/' + u1

            params = {'search': 1}
            params['url'] = u
            params['title'] = t1
            link = util.makeLink(params)
            util.addMenuItem(params['title'], link, None, None, True)
        util.endListing()
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to create menu' % (url))

def helpme():
    message = '1- on Kodi Home Goto System\n \n 2- select Appearence \n \n 3- from " Skin " \n \n " -font " select "Arial based" \n \n 4- from "International" \n  \n  "characterset"  select " Arabic(windows) " \n \n \n         Thats All ! \n \nFor More Help go to "https://sites.google.com/site/kokiarbic/help"'
    dialog = xbmcgui.Dialog()
    hp = dialog.textviewer('Help:',message)
    return hp

def home():
    
    
    action = {'new':0,'page':1}
    t = 'أفلام عربية  جديدة'
    title = (t).decode('utf-8')
    link = util.makeLink(action)
    util.addMenuItem(title, link, fanart, None, True)

    action = {'old':0,'page':1}
    t = 'زمن الفن الجميل '
    title = (t).decode('utf-8')
    link = util.makeLink(action)
    util.addMenuItem(title, link, fanart, None, True)  

    action = {'spec':1,'page':1}
    t = 'أفلام عربية للكبار '
    title = (t).decode('utf-8')
    link = util.makeLink(action)
    util.addMenuItem(title, link, fanart, None, True)

    action = {'srch':0}
    t = 'SEARCH '
    title = (t).decode('utf-8')
    link = util.makeLink(action)
    util.addMenuItem(title, link, icon, None, True)

    action = {'hlp':1}
    t = 'If you could not Read List: click here:>> '
    title = (t).decode('utf-8')
    link = util.makeLink(action)
    util.addMenuItem(title, link, icon, None, True)

    util.endListing() 


fanart = 'special://home/addons/plugin.video.koki/fanart.jpg'
icon = 'special://home/addons/plugin.video.koki/icon.png'
ADDON_ID = 'plugin.video.koki'


parameters = util.parseParameters()
if parameters:
        if 'new' in parameters:
            pages(parameters)
   
        elif 'old' in parameters:
            old(parameters)

        elif 'spec' in parameters:
            special(parameters)

        elif 'srch' in parameters:
            search()

        elif 'hlp' in parameters:
            helpme()
        
        elif 'search' in parameters:
            searchp(parameters)
        elif 'listing' in parameters:
            # Display the list of videos in a provided category.
            menuLink(parameters) 
        elif 'olo' in parameters:
            ololink(parameters)
        elif 'play' in parameters:
            # Play a video from a provided URL.
            playVideo(parameters)

else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
    home()

