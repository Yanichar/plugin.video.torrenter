# -*- coding: utf-8 -*-
'''
    Torrenter plugin for XBMC
    Copyright (C) 2012 Vadim Skorba
    vadim.skorba@gmail.com

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
import re
import Content

class ThePirateBaySe(Content.Content):
    category_dict = {
        'tvshows': ('TV Shows', '/browse/205', {'page': '/browse/208/%d', 'increase': 1, 'second_page': 1,
                                         'sort':[{'name':'by Seeders', 'url_after':'/7'},
                                                 {'name':'by Date', 'url_after':'/3'}]}),
        'tvshowshd': ('TV Shows [HD]', '/browse/208', {'page': '/browse/208/%d', 'increase': 1, 'second_page': 1,
                                         'sort':[{'name':'by Seeders', 'url_after':'/7'},
                                                 {'name':'by Date', 'url_after':'/3'}]}),
        'movies': ('Movies', '/browse/201', {'page': '/browse/208/%d', 'increase': 1, 'second_page': 1,
                                         'sort':[{'name':'by Seeders', 'url_after':'/7'},
                                                 {'name':'by Date', 'url_after':'/3'}]}),
        'movieshd': ('Movies [HD]', '/browse/207', {'page': '/browse/208/%d', 'increase': 1, 'second_page': 1,
                                         'sort':[{'name':'by Seeders', 'url_after':'/7'},
                                                 {'name':'by Date', 'url_after':'/3'}]}),
    }

    baseurl = "https://thepiratebay.se"
    headers = [('User-Agent',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124' + \
                ' YaBrowser/14.10.2062.12061 Safari/537.36'),
               ('Referer', 'http://kickass.so/'), ('Accept-Encoding', 'gzip')]
    '''
    Weight of source with this searcher provided.
    Will be multiplied on default weight.
    Default weight is seeds number
    '''
    sourceWeight = 1

    def isLabel(self):
        return True

    def isScrappable(self):
        return False

    def isInfoLink(self):
        return False

    def isPages(self):
        return True

    def isSort(self):
        return True

    def isSearchOption(self):
        return False

    def get_contentList(self, category, subcategory=None, apps_property=None):
        contentList = []
        url = self.get_url(category, subcategory, apps_property)
        print str(url)

        response = self.makeRequest(url, headers=self.headers)

        if None != response and 0 < len(response):
            #print response
            if category:
                contentList = self.mode(response)
        #print str(contentList)
        return contentList

    def mode(self, response):
        contentList = []
        #print str(result)
        num = 31
        result = re.compile(
                r'''<div class="detName">.+?">(.+?)</a>.+?<a href="(.+?)".+?<font class="detDesc">Uploaded (.+?), Size (.+?), .+?</font>.+?<td align="right">(\d+?)</td>.+?<td align="right">(\d+?)</td>''',
                re.DOTALL).findall(response)
        for (title, link, date, size, seeds, leechers) in result:
            info = {}
            num = num - 1
            if not re.match('^https?\://.+', link) and not re.match('^magnet\:.+', link):
                link = re.search('^(https?\://.+?)/.+', self.baseurl).group(1) + link
            original_title = None
            year = 0
            img = ''
            size = size.replace('&nbsp;', ' ')
            date = self.stripHtml(date.replace('&nbsp;', ' '))

            #info

            info['label'] = info['title'] = self.unescape(title)
            info['link'] = link
            info['plot'] = info['title']+'\r\n[I](%s) [S/L: %s/%s] [/I]\r\n%s' % (size, seeds, leechers, date)

            contentList.append((
                int(int(self.sourceWeight) * (int(num))),
                original_title, title, int(year), img, info,
            ))
        return contentList
