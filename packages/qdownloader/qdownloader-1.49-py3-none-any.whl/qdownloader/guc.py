#!/usr/bin/env python

from __future__ import print_function

import sys
import os
if sys.version_info.major == 2:
    from urlparse import urlparse
    from urllib import quote, unquote
else:
    from urllib.parse import urlparse, quote, unquote
import re
import  urllib
import clipboard

from pydebugger.debug import debug
from make_colors import make_colors
from bs4 import BeautifulSoup as bs

import requests
import traceback
from proxy_tester import proxy_tester

SEARCH_RESUL = None

def download(url, download_path=None):
    if sys.platform == 'win32':
        try:
            import idm
            IDM = idm.IDMan()
            IDM.download(url, download_path)
        except:
            import wget
            try:
                wget.download(url)
            except:
                print(make_colors('ERROR', 'lightwhite', 'lightred'))
                sys.exit(0)
    else:
        from pyget import wget
        wget.download(url)

def convert(url, downloadit=False, download_path=None, test=None, clip=True):
    debug(url=url)
    if test:
        # # url = "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=11&cad=rja&uact=8&ved=2ahUKEwie472y8sbfAhVBSX0KHX6ICNIQwqsBMAp6BAgDEAQ&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DhkyfnQ4GHgs&usg=AOvVaw0aUMzh5On-Lfda-T5AGDRo"
        url = "https://www.google.com/imgres?imgurl=http%3A%2F%2Fcdn2.tstatic.net%2Fjabar%2Ffoto%2Fbank%2Fimages%2F20-ucapan-selamat-tahun-baru-2019-dalam-bahasa-indonesia-dan-inggris.jpg&imgrefurl=http%3A%2F%2Fjabar.tribunnews.com%2F2018%2F12%2F28%2F20-ucapan-selamat-tahun-baru-2019-dalam-bahasa-indonesia-dan-inggris-tinggal-copy-paste-saja&docid=d0EkSSzP0ies4M&tbnid=eMmFqqzkbvU-cM%3A&vet=10ahUKEwjm28WZpsnfAhUQi3AKHbzoC5AQMwg-KAAwAA..i&w=700&h=393&itg=1&safe=strict&client=firefox-b-ab&bih=664&biw=1366&q=selamat%20tahun%20baru&ved=0ahUKEwjm28WZpsnfAhUQi3AKHbzoC5AQMwg-KAAwAA&iact=mrc&uact=8"
        debug(url=url)

    # print "url =", url
    url = urlparse(url)
    debug(url=url)
    query = re.findall('http.*?&', url.query)
    # query1 = re.findall('url=http.*?&', url.query)
    debug(query=query)
    # debug(query1=query1)
    if len(query) > 0:
        url = unquote(query[0])[:-1]
        print(make_colors("RESULT: ", 'black', 'lightgreen'), url)
        debug(url=url)
        if clip:
            clipboard.copy(url)
        if downloadit:
            download(url, download_path)
        # print "url =", url
        return url
    else:
        return False

def search(query,  use_proxy=False, proxies={}):
    debug()
    if use_proxy and not proxies:
        pt = proxy_tester.proxy_tester()
        proxy = pt.test_proxy_ip('https://www.google.com/search?q=' + query, limit=1)
        if proxy:
            proxy_host, proxy_port = proxy[0].split(":")
            proxies = {'http':'http://' + proxy_host + ":" + proxy_port, 'https':'https://' + proxy_host + ":" + proxy_port}

    elif not use_proxy and proxies:
        proxies = {}
    print("proxies =", proxies)
    a = requests.get('https://www.google.com/search?q=' + query, proxies=proxies)
    debug(url=a.url)
    b = bs(a.content, 'lxml')
    print("b =", b)
    debug(b=b)
    div_class_g = b.find_all('div', {'class':'g'})
    debug(div_class_g=div_class_g)
    all_links = []
    if div_class_g:
        for i in div_class_g:
            link = i.find('a').get('href')
            title = i.find('a').text
            all_links.append([links, title])
    debug(all_links=all_links)
    return all_links

def setProxy(address):
    if ":" in address:
        host, port = str(address).split(":")
        proxies = {
                    'http':'http://' + host + ":" + port, 
                        'https':'https://' + host + ":" + port
                }
        return proxies

def usage():
    global SEARCH_RESULT
    SEARCH_RESULT = None
    use_proxy = False
    proxies = {}
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('URL', help='Full Google Url Search, type "c" only for get url from clipboard', action='store', nargs='*')
    parser.add_argument('-d', '--download', help='Download it', action='store_true')
    parser.add_argument('-p', '--download-path', help='Save download to', action='store')
    parser.add_argument('-s', '--search', help='Search like google search', action='store')
    parser.add_argument('-x', '--proxy', help='Use proxy, format: HOST:IP', action='store')
    parser.add_argument('-X', '--use-proxy', help='Use auto proxy', action='store_true')
    if len(sys.argv) == 1:
        parser.print_usage()
    if '-s' in sys.argv:
        download_path = os.getcwd()
        if '-x' in sys.argv:
            if not sys.argv[sys.argv.index('-x') + 1] == '-d' and not sys.argv[sys.argv.index('-x') + 1] == '-p':
                proxies = setProxy(sys.argv[sys.argv.index('-x') + 1])
                use_proxy = True
        if '-X' in sys.argv:
            use_proxy=True
            debug(use_proxy_x=use_proxy)
        if '-d' in sys.argv:
            is_download = True
        if '-p' in sys.argv:
            try:
                download_path = sys.argv[sys.argv.index('-p') + 1]
            except:
                downwload_path = os.getcwd()
        try:
            debug(use_proxy=use_proxy)
            debug(proxies=proxies)
            debug(query = sys.argv[sys.argv.index('-s') + 1])
            SEARCH_RESULT = search(sys.argv[sys.argv.index('-s') + 1], use_proxy, proxies)
        except:
            if os.getenv('DEBUG_SERVER') == '1':
                print("ERROR 001 =", traceback.format_exc())
                print(make_colors("No Search Query !", 'lightred', 'lightwhite'))

    if SEARCH_RESULT:
        n = 1
        for i in SEARCH_RESULT:
            print(str(n) + ". " + i[1])
            n += 1
            q = raw_input('Select Number to Convert:')
            if q:
                convert(SEARCH_RESULT[int(str(q).strip()) - 1][0], is_download, download_path) 
    else:
        args = parser.parse_args()
        debug(args=args)
        if args.URL == ['c']:
            URL = str(clipboard.paste())
            debug(URL=URL)
            convert(URL, args.download, args.download_path)
        else:
            for URL in args.URL:
                convert(URL, args.download, args.download_path)

if __name__ == '__main__':
    # if len(sys.argv) == 1:
    # 	print "USAGE:", "FULL_GOOGLE_URL"
    # 	sys.exit(0)
    # if sys.argv[1] == 'c':
    # 	url = clipboard.paste()
    # else:
    # 	url = sys.argv[1]
    # convert(url)
    # # convert(None, False)
    usage()
