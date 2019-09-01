# -*- coding: utf-8 -*-
# @author i62gorej@uco.es 	José Luis Gordillo Relaño
from urllib.request import urlopen, urlretrieve
import urllib.request  as urllib2
from bs4 import BeautifulSoup
from random import choice
import re, os, json
import requests
import sys

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]
# Different types of image and video formats
listImages = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
listVideos = ['.mp4', '.avi', '.mkv', '.flv']

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain
        r'localhost|' #localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # or ip
        r'(?::\d+)?' # port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

# Object to evade protecction of some websites
class Opener(urllib2.FancyURLopener):
    version = choice(user_agents)

def Scraping(url):
    if re.match(regex, url) is not None:
        directory = input('Write a directory name where save all pics: ')

        # Create directory structure photo and video
        try:
            os.stat(os.path.dirname(os.path.abspath(__file__))+"\\"+directory)
        except:
            os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "\\" + directory)
            os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "\\" + directory + "\\photos")
            os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "\\" + directory + "\\videos")

        # User inserted a hispachan url
        if url.find('hispachan') != -1:
            opener = Opener()
            page = opener.open(url)
            soup = BeautifulSoup(page.read(), 'html.parser')

            linkers = soup.findAll('a', attrs={'href': re.compile("^https://www.hispachan.org/")})
            print("Extracting all files into " + directory + " directory.")

            for link in list(set(linkers)):
                ext = os.path.splitext((link.get('href')))[-1].lower()
                if ext in listImages:
                    with open(os.path.join("./" + directory + "/photos/", os.path.basename(link.get('href'))),
                                  'wb') as f:
                        response = requests.get(link.get('href'))
                        f.write(response.content)
                else:
                    if ext in listVideos:
                        with open(os.path.join("./" + directory + "/videos/", os.path.basename(link.get('href'))),
                                      'wb') as f:
                            response = requests.get(link.get('href'))
                            f.write(response.content)

		# User inserted a 4chan url                            
        elif url.find('4chan') != -1 or url.find('4channel') != -1:
            opener = Opener()
            page = opener.open(url)
            soup = BeautifulSoup(page.read(), 'html.parser')

            linkers = soup.findAll('a', attrs={'href': re.compile("^//is2.4chan.org/")})
            print("Extracting all files into " + directory + " directory.")

            for link in list(set(linkers)):
                ext = os.path.splitext((link.get('href')))[-1].lower()
                if ext in listImages:
                    with open(os.path.join("./" + directory + "/photos/", os.path.basename(link.get('href'))),
                                  'wb') as f:
                        response = requests.get("http:"+link.get('href'))
                        f.write(response.content)
                else:
                    if ext in listVideos:
                        with open(os.path.join("./" + directory + "/videos/", os.path.basename(link.get('href'))),
                                      'wb') as f:
                            response = requests.get("http:" + link.get('href'))
                            f.write(response.content)
		
		# User inserted a VK URL                   
        elif url.find('vk') != -1:
            headers = {"Referer": "https://m.vk.com/login?role=fast&to=&s=1&m=1&email=YOUR_EMAIL"
                , 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0'}
            # Change email-username and password by your user in VK website
            payload = {'email': 'EMAIL', 'pass': 'PASSWORD'}
            # VK LOGIN COULD BE NECESARY IN CASE THE ACCOUNT BE PRIVATE

            if payload['email'] == 'EMAIL' or payload['pass'] == 'PASSWORD':
                print("ERROR: PAYLOAD PARAMETERS NOT CONFIGURED IN VK")
                exit(-1)
            with requests.Session() as S:
                Loginpage = S.get('https://m.vk.com/login')
                Loginsoup = BeautifulSoup(Loginpage.content, 'lxml')
                Loginurl = Loginsoup.find('form')['action']
                p = S.post(Loginurl, data=payload, headers=headers)
                # NOW YOU ARE SUCCESSFULLY LOGGED IN

                if "/videos" in url:
                    soup = BeautifulSoup(S.get(url).content, 'html.parser')
                    linkers  = soup.findAll('a', attrs={'class': 'video_item_title', 'href': re.compile("^/video")})
                    print("Extracting all files into " + directory + " directory.")

                    for linker in list(set(linkers)):
                        page = urlopen("https://vk.com"+linker.get('href'))
                        content = page.read()
                        link = content.decode('utf-8', "ignore")
                        string = re.compile('<source src=\\\\"([^"]*)\\\\"')
                        urls = string.findall(link)

                        # Extracting qualities found in video
                        for i in ['1080.mp4', '720.mp4', '360.mp4']:
                            for newUrl in urls:
                                if i in newUrl:
                                    source = newUrl.replace('\\/', '/')
                                    reg = re.compile(r'/([^/]*\.mp4)')
                                    name = reg.findall(source)[0]
                                    path = os.path.join("./" + directory + "/videos/")
                                    fullpath = os.path.join(path, name)
                                    urlretrieve(source, fullpath)

                elif "/video" in url:
                    # converting part
                    if "http://" in url:
                        url = url.replace("http", "https")
                    if "z=" in url:
                        url = url.split("z=", 1)[-1]
                        url = url.split("%2F", 1)[0]
                        url = "https://vk.com/" + url
                    page = urlopen(url)

                    content = page.read()
                    link = content.decode('utf-8', "ignore")
                    string = re.compile('<source src=\\\\"([^"]*)\\\\"')
                    urls = string.findall(link)

                    for i in ['1080.mp4', '720.mp4', '360.mp4']:
                        for newUrl in urls:
                            if i in newUrl:
                                source = newUrl.replace('\\/', '/')
                                reg = re.compile(r'/([^/]*\.mp4)')
                                name = reg.findall(source)[0]
                                path = os.path.join("./" + directory + "/videos/")
                                fullpath = os.path.join(path, name)
                                urlretrieve(source, fullpath)

                elif "/album" in url:

                    soup = BeautifulSoup(S.get(url).content, 'html.parser')
                    linkers = soup.findAll('a', attrs={'href': re.compile("^/photo")})
                    print("Extracting all files into " + directory + " directory.")
                    for link in linkers:
                        print(link.get('href'))
                        # Continue downloading image albums
                else:
                    print("Not valid url for VK")
        # Website not found           
        else:
            print('Not found the website.')
        print("Done")
    else:
        print("The URL is not correct.")

# Initialice Program
if len(sys.argv) < 2:
    print("Arguments are invalid, must insert a URL")
    exit(-1)

Scraping(sys.argv[1])
