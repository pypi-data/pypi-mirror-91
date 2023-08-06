#!/usr/bin/env python2
# encoding:utf-8
# youtube downloader
# Author: cumulus13
# email: cumulus13@gmail.com

from __future__ import print_function
import requests
from bs4 import BeautifulSoup as bs
from make_colors import make_colors
from pydebugger.debug import debug
import re
import random
import os
import sys
import getpass
import traceback
#sys.excepthook = traceback.format_exc
import clipboard
import time
import platform
from pprint import pprint
from safeprint import print as sprint
from xnotify import notify
from . import guc
from youtube_dl import YoutubeDL
from configset import configset
import progressbar

try:
    from pause import pause
except:
    # raw_input("enter to continue")
    def pause():
        return None

from datetime import datetime
if sys.version_info.major > 2:
    raw_input = input


class MyLogger(object):
    notif = notify()
    prefix = '{variables.task}::{variables.subtask}'
    # prefix = '{variables.task} >> {variables.subtask}'
    variables = {'task': '--', 'subtask': '--'}
    bar = progressbar.ProgressBar(max_value = 100, prefix = prefix, variables = variables)     
    nbar = 1    

    def __init__(self, verbose = False):
        self.verbose = verbose

    def format_msg(self, msg):
        msg = msg[:msg.find("[youtube]")] + make_colors("[youtube]", 'ly') + msg[msg.find("[youtube]") + len('[youtube]'):]        
        msg = msg[:msg.find("Downloading")] + make_colors("Downloading", 'lc') + msg[msg.find("Downloading") + len('Downloading'):]
        msg = msg[:msg.find("Finished")] + make_colors("Finished", 'lw', 'lr') + msg[msg.find("Finished") + len('Finished'):]
        return msg

    def debug(self, msg):
        bmax = 100
        if self.verbose:
            print(make_colors(datetime.strftime(datetime.now(), '%Y/%m/%d - %H:%M:%S:%f'), 'lw', 'm') + " - " + msg)
        else:
            msg1 = re.findall("\d+.*?\d+", msg)
            msg2 = str(msg[10:20])
            if msg1 and " of " in msg1[0]:
                # print("msg1 =", msg1)
                sf = msg1[0].lower().split('of')
                self.nbar = int(sf[0].strip())
                bmax = int(sf[1].strip())
                self.bar.max_value = bmax
                # msg2 = self.nbar

            task = make_colors("Generate", 'lw', 'bl')
            subtask = make_colors(str(msg2), 'lw', 'bl')
            if bmax:
                if self.nbar > bmax:
                    self.nbar = bmax
                elif self.nbar == bmax:
                    self.nbar = bmax
            elif self.nbar == 100:
                self.nbar = 1
            try:
                self.bar.update(self.nbar, task = task, subtask = subtask)
            except:
                pass
            self.nbar +=1

    def warning(self, msg):
        if self.verbose:
            print(make_colors(datetime.strftime(datetime.now(), '%Y/%m/%d - %H:%M:%S:%f'), 'lw', 'lr') + " - " + msg)
        else:
            task = make_colors("Generate warning", 'lw', 'bl')
            subtask = make_colors(str(msg[:12]), 'b', 'ly') + " "
            self.bar.update(self.nbar, task = task, subtask = subtask)
            if self.nbar == 100:
                self.nbar = 1
            self.nbar +=1
            

    def error(self, msg):
        if self.verbose:
            print(make_colors(datetime.strftime(datetime.now(), '%Y/%m/%d - %H:%M:%S:%f'), 'lw', 'lr') + " - " + make_colors(msg, 'lr', 'lw'))
        else:
            task = make_colors("Generate error", 'lw', 'bl')
            subtask = make_colors(str(msg[:12]), 'lw', 'lr') + " "
            self.bar.update(self.nbar, task = task, subtask = subtask)
            if self.nbar == 100:
                self.nbar = 1
            self.nbar +=1
        self.notif.notify("Download Error: ", msg, "qDownloader", "ERROR")
        return False

if sys.version_info.major == 3:
    raw_input = input
BACK_RANDOM = ['lightyellow', 'lightcyan']

class qdownloader(object):

    opt = {
        'simulate':True, 
        'format':'mp4', 
        'forcetitle':True, 
        'writethumbnail':True,
        'logger': MyLogger(),
    }
    youtube = YoutubeDL(opt)
    configfile = os.path.join(os.path.dirname(__file__), 'qdownloader.ini')
    config = configset(configfile)

    prefix = '{variables.task}::{variables.subtask}'
    # prefix = '{variables.task} >> {variables.subtask}'
    variables = {'task': '--', 'subtask': '--'}
    bar = progressbar.ProgressBar(max_value = 100, prefix = prefix, variables = variables)     
    current_thread = []

    def __init__(self, download_path = os.getcwd()):
        super(qdownloader, self)
        self.URL = 'https://qdownloader.io/download'
        self.download_path = download_path
        self.LINKS = {}

    @classmethod
    def downloader(cls, url, download_path = None, saveas = None, confirm = False):
        debug(download_path = download_path)
        if os.getenv('DOWNLOAD_PATH'):
            download_path = os.getenv('DOWNLOAD_PATH')
        debug(download_path = download_path)
        if not download_path:
            download_path = cls.config.get_config('DOWNLOAD', 'path', os.getcwd())
            debug(download_path = download_path)
        if 'linux' in sys.platform:
            if not os.path.isdir(download_path):
                this_user = getpass.getuser()
                login_user = os.getlogin()
                debug(login_user = login_user)
                this_uid = os.getuid()
                download_path = r"/home/{0}/Downloads".format(login_user)
                debug(download_path = download_path)
                if not os.path.isdir(download_path):
                    try:
                        os.makedirs(download_path)
                    except OSError:
                        print(make_colors("Permission failed make dir:", 'lw', 'lr', ['blink']) + " " + make_colors(download_path, 'lr', 'lw'))
        try:
            if not os.path.isdir(download_path):
                download_path = os.getcwd()
        except:
            download_path = None
            pass

        if not download_path:
            download_path = os.getcwd()
        if not os.access(download_path, os.W_OK|os.R_OK|os.X_OK):
            print(make_colors("You not have Permission save to dir:", 'lw', 'lr' + " " + make_colors(download_path, 'lr', 'lw')))
            download_path = os.getcwd()
        print(make_colors("DOWNLOAD PATH:", 'lw', 'bl') + " " + make_colors(download_path, 'lw', 'lr'))

        debug(url = url)
        cls.download(url, download_path, saveas, confirm)
        icon = None
        if os.path.isfile(os.path.join(os.path.dirname(__file__), 'logo.png')):
            icon = os.path.join(os.path.dirname(__file__), 'logo.png')

        cls.notify.notify("Download finish: ", saveas, "ydl", "FINISH", iconpath = icon)

        return url

    @classmethod
    def download_linux(cls, url, download_path=os.getcwd(), saveas=None, downloader = 'aria2c'):
        '''
            downloader: aria2c, wget, uget, persepolis
        '''
        # if cls.is_vimeo:
        #     downloader = 'wget'
        if sys.version_info.major == 3:
            aria2c = subprocess.getoutput("aria2c")
        else:
            aria2c = os.popen3("aria2c")[2].readlines()[0]
        if sys.version_info.major == 3:
            wget = subprocess.getoutput("wget")
        else:
            wget = os.popen3("wget")[2].readlines()[0]
        if sys.version_info.major == 3:
            persepolis = subprocess.getoutput("persepolis --help")
        else:
            persepolis = os.popen3("persepolis --help")[1].readlines()[0]

        if downloader == 'aria2c' and not re.findall("not found\n", aria2c):
            if saveas:
                saveas = '-o "{0}"'.format(saveas)
            cmd = 'aria2c -c -d "{0}" "{1}" {2} --file-allocation=none'.format(os.path.abspath(download_path), url, saveas)
            debug(cmd = cmd)
            os.system(cmd)
        elif downloader == 'wget' and not re.findall("not found\n", wget):
            if saveas:
                saveas = '-P "{0}" -O "{1}"'.format(os.path.abspath(download_path), saveas)
            else:
                saveas = '-P "{0}"'.format(os.path.abspath(download_path))
            cmd = 'wget -c "{0}" {1}'.format(url, saveas)
            debug(cmd = cmd)
            os.system(cmd)
        elif downloader == 'persepolis'  and not re.findall("not found\n", persepolis):
            cmd = 'persepolis --link "{0}"'.format(url)
            debug(cmd = cmd)
            os.system(cmd)
        else:
            try:
                from pywget import wget as d
                d.download(url, download_path, saveas)
            except:
                print(make_colors("Can't Download this file !, no Downloader supported !", 'lw', 'lr', ['blink']))
                clipboard.copy(url)

    @classmethod
    def download(cls, url, download_path=os.getcwd(), download_name=None, confirm=False):
        debug(url = url)
        if not os.path.isdir(download_path):
            try:
                os.makedirs(download_path)
            except:
                pass
        # pause()
        if sys.platform == 'win32':
            try:
                from idm import IDMan
                dm = IDMan()
                dm.download(url, download_path, download_name, confirm=confirm)
            except:
                from pywget import wget
                if download_name:
                    print(make_colors("Download Name:", 'lw', 'bl') + " " + make_colors(download_name, 'lw', 'm'))
                    download_path = os.path.join(download_path, download_name)
                wget.download(url, download_path)
        elif 'linux' in sys.platform:
            return cls.download_linux(url, download_path, download_name)
        else:
            print(make_colors("Your system not supported !", 'lw', 'lr', ['blink']))

    @classmethod
    def get_info(cls, url):
        if urlparse(url).netloc == 'vimeo.com':
            cls.is_vimeo = True
        if 'list=PL' in url:
            cls.is_playlist = True
        try:
            result = cls.youtube.extract_info(url)
            return result
        except:
            return False

    def getContent(self, url):
        params = {'url': url}
        a = requests.get(self.URL, params=params)
        if a.status_code == 200:
            return a.content
        else:
            return False

    def pcloud(self, url, download_path=os.getcwd(), name=None, username=None, password=None, folderid='0', foldername=None):
        from pyPCloud import pcloud
        PCloud = pcloud()
        while 1:
            try:
                datax = PCloud.remoteUpload(url, username=username, password=password,folderid=folderid, renameit=name, foldername=foldername)
                idx = datax.get('metadata')[0].get('id')
                data, cookies = PCloud.getDownloadLink(idx, download_path=download_path)
                download_url = 'https://' + data.get('hosts')[0] + data.get('path')
                return download_url
            except:
                print (traceback.format_exc())
                return self.pcloud(url, download_path, name, username, password, folderid, foldername)
                
    def get_index(self, url):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
        }
        a = requests.get(url, headers = headers)
        b = bs(a.content, 'lxml')
        items = b.find('div', {'class': re.compile("playlist-items"), 'id':"items"})
        debug(items = items )
        alink = items.find_all('a', id="wc-endpoint")
        debug(alink = alink)

    def download_chanel(self, url, quality_search=None, with_sound=True, download_path=os.getcwd(), download_name=None, pcloud=False, qs=None, download_it=False, start_from= 0, end_to = None, max_try= 10, download_thread = False, overwrite = False):
        finish = False
        sys.stdout.flush()
        print("\r" + make_colors("DOWNLOAD_PATH", 'lightwhite', 'blue') + ": " + make_colors(download_path, 'lightcyan'))
        debug(url = url)
        # current_thread = []
        current_thread_max = 0
        example_link = "Example Link: https://www.youtube.com/playlist?list=PL-CtdCApEFH-7hBhz1Q-4rKIQntJoBNX3"
        if not "playlist?list=" in url:
            self.getLinks(url, quality_search=quality_search, with_sound=with_sound, download_path=download_path, download_name=download_name, pcloud=pcloud, qs=qs, download_it=download_it)

        all_links = []
        nt = 0
        entries = None
        # entries = self.youtube.extract_info(url).get('entries')
        try:
            entries = self.youtube.extract_info(url)
        except:
            print(traceback.format_exc())
            tp, vl, tb = sys.exc_info()
            if vl.__class__.__name__ == "DownloadError":
                return self.download_chanel(url, quality_search, with_sound, download_path, download_name, pcloud, qs, download_it, start_from, end_to, max_try, download_thread, overwrite)
            else:
                print("ERROR:", vl.__class__.__name__)
                pause()
        while 1:
            try:
                if entries:
                    entries = entries.get('entries')
                    break
            except:
                time.sleep(1)
                entries = self.youtube.extract_info(url)

        while 1:
            if not entries:
                if nt == max_try:
                    break
                else:
                    nt += 1
                entries = self.youtube.extract_info(url)
            else:
                break
        debug(entries = entries)
        
        for i in entries:
            # print("i =", i)
            try:
                yid = i.get('id')
                name = i.get('title') + ".mp4"
                index = i.get('playlist_index')
                all_links.append(['https://www.youtube.com/watch?v={0}'.format(yid), name, index])
            except:
                pass
        
        debug(all_links=all_links)
        # print ("all_links =", all_links)

        if isinstance(start_from, str):
            start_from = int(start_from)
        if isinstance(start_from, bool):
            start_from = 0
        if isinstance(end_to, str):
            end_to = int(end_to)
        if isinstance(end_to, bool):
            end_to = 0
        # start_from = start_from - 1
        debug(all_links=all_links)
        debug(start_from = start_from)
        debug(end_to = end_to)
        if not end_to:
            end_to = None
        else:
            end_to = end_to - 1
        
        if start_from:
            start_from = start_from - 1
        if start_from > len(all_links):
            print(make_colors("Max video length is {}".format(len(all_links)), 'lw', 'lr'))
            sys.exit()
        def generate_name(link, all_links):
            name = None
            if not isinstance(link, list):
                return None
            if link[2] < 10 and len(all_links) < 100:
                name = "0" + str(link[2]) + ". " + link[1]
            elif link[2] > 10 and link[2] < 100 and len(all_links) <= 100:
                name = str(link[2]) + ". " + link[1]
            elif link[2] < 10 and len(all_links) > 100:
                name = "00" + str(link[2]) + ". " + link[1]
            elif link[2] > 10 and link[2] < 100 and len(all_links) >= 100:
                name =  "0" + str(link[2]) + ". " + link[1]
            else:
                name =  str(i[2]) + ". " + i[1]
            name = re.sub(":", "-", name)
            name = re.sub("/", "_", name)
            name = re.sub("\|", "-", name)
            name = re.sub("\?", "-", name)
            return name

        nbar = 1
        debug(all_links = all_links)
        debug(start_from = start_from)
        debug(end_to = end_to)
        debug(all_links_cut = all_links[start_from:end_to])
        
        current_thread_max = len(all_links[start_from:end_to])
        for i in all_links[start_from:end_to]:
            name = generate_name(i, all_links)
            self.bar.max_value = len(all_links[start_from:end_to])
            # print("\n")
            # print("-"*100)
            debug(i = i)
            debug(download_thread = download_thread)
            debug(name = name)
            debug(download_path = download_path)
            debug(save_as = os.path.join(download_path, name))

            if download_thread:
                debug(download_thread = download_thread)
                debug(current_thread = self.current_thread)
                debug(current_thread_max = current_thread_max)
                if not self.current_thread:
                    debug(current_thread = self.current_thread)
                    self.current_thread.append(os.path.join(download_path, name))
                    debug(current_thread = self.current_thread)
                    debug(current_thread_max = current_thread_max)
                    current_thread_max -= 1
                    debug(current_thread_max = current_thread_max)

                    task = make_colors("Downloading", 'b', 'ly')
                    subtask = make_colors(str(name), 'lw', 'lr') + " "                    
                    self.bar.update(nbar, task = task, subtask = subtask)

                    debug(save_as = os.path.join(download_path, name))
                    if not os.path.isfile(os.path.join(download_path, name)):
                        self.getLinks(i[0], False, quality_search, with_sound, download_path, name, pcloud, qs, download_it)
                    else:
                        if overwrite:
                            self.getLinks(i[0], False, quality_search, with_sound, download_path, name, pcloud, qs, download_it)
                            task = make_colors("Downloading", 'b', 'lg') + " " + make_colors("[Overwrite]", 'lw', 'lr')
                            self.bar.update(nbar, task = task, subtask = subtask)
                        else:
                            task = make_colors("Downloaded", 'b', 'lg')
                            self.bar.update(nbar, task = task, subtask = subtask)
                    if nbar == len(all_links[start_from:end_to]):
                        break
                    else:
                        nbar +=1
                    
                    if current_thread_max == 0:
                        break
                if len(self.current_thread) < download_thread:
                    debug(current_thread = self.current_thread)
                    self.current_thread.append(os.path.join(download_path, name))
                    debug(current_thread = self.current_thread)
                    debug(current_thread_max = current_thread_max)
                    current_thread_max -= 1
                    debug(current_thread_max = current_thread_max)

                    task = make_colors("Downloading", 'b', 'ly')
                    subtask = make_colors(str(name), 'lw', 'lr') + " "
                    
                    self.bar.update(nbar, task = task, subtask = subtask)

                    if not os.path.isfile(os.path.join(download_path, name)):
                        self.getLinks(i[0], False, quality_search, with_sound, download_path, name, pcloud, qs, download_it)
                    else:
                        if overwrite:
                            self.getLinks(i[0], False, quality_search, with_sound, download_path, name, pcloud, qs, download_it)
                            task = make_colors("Downloading", 'b', 'lg') + " " + make_colors("[Overwrite]", 'lw', 'lr')
                            self.bar.update(nbar, task = task, subtask = subtask)
                        else:
                            task = make_colors("Downloaded", 'b', 'lg')
                            self.bar.update(nbar, task = task, subtask = subtask)
                    if nbar == len(all_links[start_from:end_to]):
                        break
                    else:
                        nbar +=1
                    
                    if current_thread_max == 0:
                        break
                elif len(self.current_thread) == download_thread:
                    debug(current_thread = self.current_thread)
                    while 1:
                        for d in self.current_thread:
                            debug(d = d)
                            if os.path.isfile(d):
                                debug(current_thread = self.current_thread)
                                self.current_thread.remove(d)
                                debug(current_thread = self.current_thread)
                                debug(current_thread_max = current_thread_max)
                                if not self.current_thread:
                                    break
                                if current_thread_max == 0:
                                    finish = True
                                    break
                            else:
                                time.sleep(5)
                    
                        if not self.current_thread:
                            break
                                
                        if current_thread_max == 0:
                            finish = True
                            break
                if finish:
                    break
            else:
                task = make_colors("Downloading", 'b', 'ly')
                subtask = make_colors(str(name), 'lw', 'lr') + " "
                self.bar.update(nbar, task = task, subtask = subtask)
                if nbar == len(all_links[start_from:end_to]):
                    nbar = 1
                else:
                    nbar +=1
                if not os.path.isfile(os.path.join(download_path, name)):
                    self.getLinks(i[0], False, quality_search, with_sound, download_path, name, pcloud, qs, download_it)
                else:
                    if overwrite:
                        self.getLinks(i[0], False, quality_search, with_sound, download_path, name, pcloud, qs, download_it)
                        task = make_colors("Downloading", 'b', 'lg') + " " + make_colors("[Overwrite]", 'lw', 'lr')
                        self.bar.update(nbar, task = task, subtask = subtask)
                    else:
                        task = make_colors("Downloaded", 'b', 'lg')
                        self.bar.update(nbar, task = task, subtask = subtask)
        nbar = 1
        return True

    def getLinks(self, url, interactive=False, quality_search=None, with_sound=True, download_path=os.getcwd(), download_name=None, pcloud=False, qs=1, download_it=False, copy_to_clipboard=False):
        #print("download_path 0 A =", download_path)
        if 'www.google.com' in url:
            url = guc.convert(url)
        if not url:
            print(make_colors("Invalid url !", 'lw' ,'lr', ['blink']))
            sys.exit()
        if not download_path or download_path == '':
            download_path = self.download_path
        if not download_path and not overwrite:
            download_path = os.getenv('DOWNLOAD_PATH')          
        if '&' in url:
            url = re.findall('https://.*?&', url)[0][:-1]
        debug(url = url)
        debug()
        debug(locals=locals())
        m = 1
        n = 1
        content = self.getContent(url)
        if not content:
            print (make_colors('Error Get Links', 'white', 'lightred'))
            sys.exit(0)
        else:
            b = bs(content, 'lxml')
            download_type = b.find_all('div', {'class': 'download-type'})
            debug(download_type = download_type)
            downloadsTable = b.find_all('table', {'class': 'downloadsTable'})
            debug(downloadsTable=downloadsTable)
            NAME = ""
            try:
                NAME = b.find('span', {'class': 'largeMargin title',}).text
                debug(NAME = NAME)
            except:
                pass
            for i in downloadsTable:
                tr = i.find_all('tr')[1:]
                try:
                    dtype = re.split("\n", download_type[m-1].text)
                    for t in dtype:
                        if str(t).strip() == '':
                            dtype.remove(t)
                    self.LINKS.update({m: {'type': dtype[0], 'links': {}}})
                except:
                    dtype = "All Download"
                    self.LINKS.update({m: {'type': dtype, 'links': {}}})
                for x in tr:
                    # print "x =",x
                    debug(x=x)
                    a_link = x.find('a')
                    debug(a_link=a_link)
                    name = a_link.get('download')
                    debug(name=name)
                    if not name:
                        name = NAME
                    if isinstance(name, bytes):
                        name = name.decode('utf-8')
                    link = a_link.get('href')
                    debug(link=link)
                    td = x.find_all('td')[:3]
                    debug(td=td)
                    quality = td[0].text
                    debug(quality=quality)
                    ext = td[1].text
                    debug(ext=ext)
                    size = td[2].text
                    debug(size=size)
                    if not 'snapdownloader' in link:
                        self.LINKS.get(m).get('links').update({
                            n: {
                                'name': name,
                                'link': link,
                                'quality': quality,
                                'ext': ext,
                                'size': size
                            }
                        })
                        n += 1
                n = 1
                m += 1

        debug(self_LINKS=self.LINKS)
        # pause()
        # print "self.LINKS =", self.LINKS
        download_url = None
        #print("download_path 0 D =", download_path)
        
        if interactive:
            self.navigator(download_path, download_name, pcloud)
        if with_sound:
            debug('with_sound')
            if quality_search:
                debug('quality_search')
                q1 = self.LINKS.get(1).get('links')
                if qs:
                    download_url = q1.get(int(qs)).get('link')
                    if copy_to_clipboard:
                        clipboard.copy(download_url)
                    if not download_name:
                        download_name = q1.get(int(qs)).get('name')
                    debug(download_url_01_1=download_url)
                    debug(download_name=download_name)
                for i in q1:
                    if q1.get(i).get('quality') == quality_search:
                        download_url = q1.get(i).get('link')
                        if copy_to_clipboard:
                            clipboard.copy(download_url)
                        debug(download_url_01_2=download_url)
                        debug(download_it=download_it)
                        debug(download_name=download_name)
                        if download_it and download_url:
                            if not download_name:
                                download_name = q1.get(i).get('name')
                            qdownloader.download(download_url, download_path, download_name, pcloud)
                        return q1.get(i)
            else:
                if qs:
                    debug(self_LINKS = self.LINKS)
                    debug(qs = qs)
                    # pause()
                    if int(qs) > len(self.LINKS.get(1).get('links').keys()):
                        print(make_colors("Invalid Quality Search !", 'lw', 'lr', ['blink']))
                        qs = raw_input(make_colors("Please insert Number Quality Search, number is integer from 1 to {0}:".format(len(self.LINKS.get(1).get('links').keys())), 'lw', 'lr') + " ")

                    download_url = self.LINKS.get(1).get('links').get(int(qs)).get('link')
                    if copy_to_clipboard:
                        clipboard.copy(download_url)
                    if not download_name:
                        download_name = self.LINKS.get(1).get('links').get(int(qs)).get('name')
                    debug(download_url_01_3=download_url)
                debug(download_it=download_it)
                debug(download_url=download_url)
                debug(download_name=download_name)
                # pause()
                if download_it and download_url:
                    qdownloader.download(download_url, download_path, download_name, pcloud)
                debug(self_LINKS = self.LINKS)
                try:
                    return self.LINKS.get(1).get('links').get(1)
                except AttributeError:
                    return self.getLinks(url, interactive, quality_search, with_sound, download_path, download_name, pcloud, qs, download_it, copy_to_clipboard)
        else:
            debug('without_sound')
            if quality_search:
                q2 = self.LINKS.get(2).get('links')
                if qs:
                    download_url = q2.get(int(qs)).get('link')
                    if copy_to_clipboard:
                        clipboard.copy(download_url)
                    if not download_name:
                        download_name = q2.get(int(qs)).get('name')
                    debug(download_url_02_1=download_url)
                    debug(download_name=download_name)
                for i in q2:
                    if q2.get(i).get('quality') == quality_search:
                        download_url = q2.get(i).get('link')
                        if copy_to_clipboard:
                            clipboard.copy(download_url)
                        debug(download_url_02_2=download_url)
                        debug(download_it=download_it)
                        debug(download_name=download_name)
                        if download_it and download_url:
                            if not download_name:
                                download_name = q2.get(i).get('name')
                            qdownloader.download(download_url, download_path, download_name, pcloud)
                        return q2.get(i)
            else:
                if qs:
                    download_url = self.LINKS.get(2).get('links').get(int(qs)).get('link')
                    if copy_to_clipboard:
                        clipboard.copy(download_url)
                    if not download_name:
                        download_name = self.LINKS.get(2).get('links').get(int(qs)).get('name')
                    debug(download_url_02_3=download_url)
                    debug(download_it=download_it)
                    debug(download_url=download_url)
                    debug(download_name=download_name)
                if download_it and download_url:
                    qdownloader.download(download_url, download_path, download_name, pcloud)
                return self.LINKS.get(2).get('links').get(1)
        debug(download_it=download_it)
        debug(download_url=download_url)
        if download_it and download_url:
            qdownloader.download(download_url, download_path, download_name, pcloud)
            
        if quality_search:
            return False
        else:
            return self.LINKS

    def downloadx(self, url, download_path=os.getcwd(), name=None, pcloud=True):
        #print("download_path 2 =", download_path)
        try:
            clipboard.copy(str(url))
        except:
            pass
        if name:
            try:
                print (make_colors('Downloading ', 'lightwhite', 'lightblue') + make_colors(name, 'lightwhite', 'lightmagenta'))
            except:
                print ("Downloading", name.encode('utf-8'))

        if not download_path:
            if os.getenv('DOWNLOAD_PATH') and os.path.isdir(os.getenv('DOWNLOAD_PATH')):
                download_path = os.getenv('DOWNLOAD_PATH')
            else:
                download_path = os.getcwd()
        if not os.path.isdir(download_path):
            os.makedirs(download_path)
        if pcloud and not 'pcloud' in url:
            n = 1
            while 1:
                try:
                    url = self.pcloud(url, download_path, name)
                    if n > 1:
                        print ("\n")
                    break
                except:
                    print (traceback.format_exc())
                    time.sleep(1)
                    sys.stdout.write("+")
                    n += 1
        debug(url=url)
        if not url:
            return qdownloader.download(url, download_path, name, pcloud)
        if sys.platform == 'win32':
            try:
                import idm
                dm = idm.IDMan()
                dm.download(url, download_path, name)
            except:
                if os.getenv('DEBUG') or os.getenv('DEBUG_EXTRA'):
                    print (traceback.format_exc())
                from pywget import wget
                if name:
                    output = os.path.join(download_path, name)
                else:
                    output = None
                wget.download(url, output)
        else:
            from pywget import wget
            if name:
                output = os.path.join(download_path, name)
            else:
                output = None
            wget.download(url, output)

    def navigator(self, download_path=os.getcwd(), download_name=None, pcloud=False):
        debug()
        n = 1
        m = 1
        v01_range = []
        v02_range = []

        if not self.LINKS:
            print (make_colors('Please run getLinks before !', 'white', 'lightred'))
            return False
        for i in self.LINKS:
            print (str(n) + ". " + make_colors(self.LINKS.get(i).get('type'), 'black', random.choice(BACK_RANDOM)) + ": ")
            for j in self.LINKS.get(i).get('links'):
                name = self.LINKS.get(i).get('links').get(j).get('name')
                if name:
                    if isinstance(name, bytes):
                        name = name.decode('utf-8')
                else:
                    name = make_colors("[NO NAME]", 'lightyellow')
                #print("name    =", name)
                name = make_colors(name, 'lightyellow')
                quality = self.LINKS.get(i).get('links').get(j).get('quality')
                if isinstance(quality, bytes):
                    quality = quality.decode('utf-8')
                size = self.LINKS.get(i).get('links').get(j).get('size')
                if isinstance(size, bytes):
                    size = size.decode('utf-8')
                ext = self.LINKS.get(i).get('links').get(j).get('ext')
                if isinstance(ext, bytes):
                    ext = ext.decode('utf-8')
                if isinstance(name, bytes):
                    name = name.decode('utf-8')
                #print("quality =", quality)
                #print("size    =", size)
                #print("ext     =", ext)
                try:
                    print(" " * 4 + str(m) + ". " + name + "[" + make_colors(quality, 'lightwhite', 'lightblue') + "|" + make_colors(size, 'black', 'lightgreen') + "|" + make_colors(ext, 'lightwhite', 'lightmagenta') + "]")
                except:
                    sprint(" " * 4 + str(m) + ". " + name + "[" + make_colors(quality, 'lightwhite', 'lightblue') + "|" + make_colors(size, 'black', 'lightgreen') + "|" + make_colors(ext, 'lightwhite', 'lightmagenta') + "]")

                if self.LINKS.get(i).get('type') == "Download Video with Sound":
                    # print "j1 =", j
                    v01_range.append(m)
                if self.LINKS.get(i).get('type') == "Download Video without Sound":
                    # print "j2 =", j
                    v02_range.append(m)
                m += 1
            n += 1
        self.notify = notify('qDownloader', 'qDownloader', 'ready', 'Ready to Download !', active_nmd = False, active_pushbullet = False, timeout = 15, direct_run = True)
        note1 = make_colors('Select Number to download  ', 'ly') +\
                make_colors("n[c] = only copy download link", 'b', 'lg') +\
                " " + ":"
        qs = raw_input(note1)
        debug(v01_range = v01_range)
        debug(v02_range = v02_range)
        copy_to_clipboard = False
        if qs[-1] == 'c':
            copy_to_clipboard = True
        debug(copy_to_clipboard = copy_to_clipboard)
        qs = qs[:-1]
        debug(qs = qs)
        if str(qs).strip().isdigit():
            if int(qs) in v01_range:
                download_url = self.LINKS.get(1).get('links').get(int(qs)).get('link')
                if copy_to_clipboard:
                    clipboard.copy(download_url)
                    return True

                if not download_name:
                    download_name = self.LINKS.get(1).get('links').get(int(qs)).get('name')

                if pcloud:
                    download_url = self.pcloud(download_url, download_path, download_name)

                qdownloader.download(download_url, download_path,download_name, pcloud)
                return download_url

            if int(qs) in v02_range:
                # qs1 = len(v02_range) - v02_range[0]
                debug(self_LINKS=self.LINKS)
                debug(qs=qs)
                # debug(qs1=qs1)
                debug(v02_range=v02_range)
                np = int(qs)-(len(self.LINKS.get(1)) + 1)
                debug(np=np)
                dlink = self.LINKS.get(2).get('links').get(np)
                debug(dlink=dlink)
                download_url = dlink.get('link')

                if copy_to_clipboard:
                    clipboard.copy(download_url)
                    return True

                if not download_name:
                    download_name = dlink.get('name')

                if pcloud:
                    download_url = self.pcloud(download_url, download_path, download_name)

                qdownloader.download(download_url, download_path,
                              download_name, pcloud)
                return download_url
        return False

    def parse_data_file(self, data_file):
        with open(data_file, 'rb') as f:
            data = []
            for i in f.readlines():
                i = re.sub("\n|\r", "", i)
                if str(i).strip() and not i.strip()[0] == "#":
                    data.append(i)
            return data

    def usage(self):
        import argparse
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('URL', help='youtube url, type "c" only for get url from clipboard', action='store', nargs='*')
        parser.add_argument('-a', '--all-channel', help='Download All of Channel URL, URL must be Channel URL', action='store_true')
        parser.add_argument('-as', '--channel-start', help='Download All of Channel URL From Part of Channel', action='store', default= 0, type=int)
        parser.add_argument('-en', '--channel-end', help='Download All of Channel URL To Part of Channel', action='store', type = int)
        parser.add_argument('-qs', '--quality-number', help='Quality Number Selected From List, default=1', action='store', default=1, type=int)
        parser.add_argument(
            '--pcloud', help='Upload to Pcloud and Download it', action='store_true')
        parser.add_argument('-p', '--download-path',
                            help='Where to download Save', action='store')
        parser.add_argument('-n', '--download-name',
                            help='Option download name Save', action='store')
        parser.add_argument('-q', '--quality',
                            help='Video quality', action='store')
        parser.add_argument('-c', '--clip', help='Copy download url/url result to clipboard', action='store_true')
        parser.add_argument(
            '-ns', '--no-sound', help='Prefer Download Video without Sound', action='store_false')
        parser.add_argument('-t', '--thread', help = "How many download every time", type = int)
        parser.add_argument('-o', '--overwrite', help='Overwrite', action='store_true')
        parser.add_argument('-v', '--verbose', action = 'store_true', help='Show debug log')
        parser.add_argument('-V', '--version', action = 'store_true', help='Show version number')
        if len(sys.argv) == 1:
            parser.print_help()
        elif len(sys.argv) == 2 and sys.argv[1] == '-V':
            from __version__ import version
            print("version: ", version)
        elif len(sys.argv) == 2 and sys.argv[1] == '--version':
            from __version__ import version
            print("version: ", version)
        else:
            args = parser.parse_args()
            download_path = args.download_path
            if args.verbose:
                self.opt.update({'logger':MyLogger(True)})
                self.youtube = YoutubeDL(self.opt)
            # if args.URL == 'c':
            #     args.URL = str(clipboard.paste())[0]
            if args.URL == ['c']:
                args.URL = list(filter(None, [x for x in re.split("\n\r| ", clipboard.paste())]))
            elif os.path.isfile(args.URL[0]):
                args.URL = self.parse_data_file(args.URL[0])

            if args.all_channel:
                for i in args.URL:
                    debug(i = i)
                    url_data = i.split("||")
                    debug(url_data = url_data)
                    if len(url_data) == 2:
                        download_path = url_data[1]
                    while 1:
                        url = "{}".format(url_data[0])
                        debug(url = url)
                        check = self.download_chanel(url, args.quality, args.no_sound, download_path, args.download_name, args.pcloud, args.quality_number, True, args.channel_start, args.channel_end, download_thread = args.thread)
                        if check:
                            break
            else:
                for i in args.URL:
                    if "||" in i:
                        url_data = i.split("||")
                        if len(url_data) == 2:
                            download_path = url_data[1]
                    else:
                        url_data = [i]
                        
                    url = "{}".format(url_data[0])
                    debug(url = url)
                    if args.quality:
                        self.getLinks(url, False, args.quality, args.no_sound, download_path, args.download_name, args.pcloud, download_it = True, copy_to_clipboard=args.clip)
                    else:                 
                        self.getLinks(url, True, args.quality, args.no_sound, args.download_path, args.download_name, args.pcloud, download_it = False, copy_to_clipboard=args.clip)

def usage():
    c = qdownloader()
    c.usage()


if __name__ == '__main__':

    PID = os.getpid()

    print ("PID:", PID)
    c = qdownloader()
    c.usage()
    # c.get_index("https://www.youtube.com/watch?v=I262xz_wtwg&list=PL88D33D34A498DFE2")
    # c.getLinks(sys.argv[1], True)
    # print "DATA =", c.getLinks(sys.argv[1], False, '360p')
