# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Aug 23 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

import wx.xrc
from urllib.request import urlopen, urlretrieve, Request
import urllib.request  as urllib2
from bs4 import BeautifulSoup
from random import choice
import re, os, json
import requests
import sys
import time
###########################################################################
## Expresions and Global Variables
###########################################################################
user_agents = [
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'},
    {'User-Agent': 'Opera/9.25 (Windows NT 5.1; U; en)'},
    {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
    {'User-Agent': 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)'},
    {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12'},
    {'User-Agent': 'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'},
]                  
# Different types of image and video formats
listImages = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
listVideos = ['.mp4', '.avi', '.mkv', '.flv', 'webm']

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 390,250 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )        
        
        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
        
        fgSizer12 = wx.FlexGridSizer( 0, 1, 0, 0 )
        fgSizer12.SetFlexibleDirection( wx.BOTH )
        fgSizer12.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        fgSizer12.SetMinSize( wx.Size( 300,200 ) ) 
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Paste the URL to download all media files:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        self.m_staticText1.SetFont( wx.Font( 18, 70, 90, 90, False, "Lucida Grande" ) )
        
        fgSizer12.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        self.txtUrl = wx.TextCtrl( self, wx.ID_ANY, '', wx.DefaultPosition, wx.Size( 300,30 ), 0 )
        self.txtUrl.SetFont( wx.Font( 18, 70, 90, 90, False, "Lucida Grande" ) )
        
        fgSizer12.Add( self.txtUrl, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.btnDownload = wx.Button( self, wx.ID_ANY, u"Download", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btnDownload.SetDefault() 
        self.btnDownload.SetFont( wx.Font( 18, 70, 90, 90, False, "Lucida Grande" ) )
    
        fgSizer12.Add( self.btnDownload, 1, wx.ALL|wx.EXPAND, 5 )
        
        bSizer7 = wx.BoxSizer( wx.VERTICAL )        

        self.txtResponse = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(300,50), 0)
        self.txtResponse.SetFont( wx.Font( 18, 70, 90, 90, False, "Lucida Grande" ) )
        bSizer7.Add( self.txtResponse, 0, wx.ALL, 5 )

        
        self.txtCredits = wx.StaticText( self, wx.ID_ANY, u"Developed by i62gorej", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txtCredits.Wrap( -1 )
        self.txtCredits.SetFont( wx.Font( 18, 70, 90, 90, False, "Lucida Grande" ) )
        
        bSizer7.Add( self.txtCredits, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        fgSizer12.Add( bSizer7, 1, wx.EXPAND, 5 )
        
        
        bSizer5.Add( fgSizer12, 0, wx.EXPAND, 5 )
        
        bSizer6 = wx.BoxSizer( wx.VERTICAL )
        
            
        bSizer5.Add( bSizer6, 1, wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer5 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.btnDownload.Bind( wx.EVT_BUTTON, self.downloadMedia )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def downloadMedia( self, event ):
        url = str(self.txtUrl.GetValue())
        cont_file = 0
        if url == '':
            self.txtUrl.SetBackgroundColour( wx.Colour( 255, 0, 0 ) )
            self.txtUrl.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
        else:
            if self.checkUrl(url):
                self.txtResponse.SetForegroundColour( wx.Colour( 34,139,34 ) ) 
                self.txtResponse.SetValue(str('Downloading media...')) 
                directory, evento = self.createDialog()                                  
                if evento == "close":
                    self.txtResponse.SetValue(str('Must introduce a folder name.')) 
                    pass
                else:
                    # Create directory structure photo and video
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                        os.makedirs("./" + directory + "/photos")
                        os.makedirs("./" + directory + "/videos")                       
                    if url.find('hispachan') != -1:                                        
                        req = urllib2.Request(url, headers=choice(user_agents))
                        page = urllib2.urlopen(req)
                        soup = BeautifulSoup(page.read(), 'html.parser')                       
                        linkers = soup.findAll('a', attrs={'href': re.compile("^https://www.hispachan.org/")})

                        for link in list(set(linkers)):
                            ext = os.path.splitext((link.get('href')))[-1].lower()
                            if ext in listImages:
                                with open(os.path.join("./" + directory + "/photos/", os.path.basename(link.get('href'))),
                                            'wb') as f:
                                    response = requests.get(link.get('href'))
                                    f.write(response.content)     
                                    cont_file+=1                       
                            else:
                                if ext in listVideos:
                                    with open(os.path.join("./" + directory + "/videos/", os.path.basename(link.get('href'))),
                                                'wb') as f:
                                        response = requests.get(link.get('href'))
                                        f.write(response.content)
                                        cont_file+=1

                    # User inserted a 4chan url                            
                    elif url.find('4chan') != -1 or url.find('4channel') != -1:
                        req = urllib2.Request(url, headers=choice(user_agents))
                        page = urllib2.urlopen(req)
                        soup = BeautifulSoup(page.read(), 'html.parser')

                        linkers = soup.findAll('a', attrs={'href': re.compile("^//is2.4chan.org/")})
                        string = "Extracting all files into " + directory + " directory."
                        self.txtResponse.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
                        self.txtResponse.SetValue(string)   

                        for link in list(set(linkers)):
                            ext = os.path.splitext((link.get('href')))[-1].lower()
                            if ext in listImages:
                                with open(os.path.join("./" + directory + "/photos/", os.path.basename(link.get('href'))),
                                            'wb') as f:
                                    response = requests.get("http:"+link.get('href'))
                                    f.write(response.content)                                
                                    cont_file+=1
                            else:
                                if ext in listVideos:
                                    with open(os.path.join("./" + directory + "/videos/", os.path.basename(link.get('href'))),
                                                'wb') as f:
                                        response = requests.get("http:" + link.get('href'))
                                        f.write(response.content)
                                        cont_file+=1
                    
                    # User inserted a VK URL                   
                    elif url.find('vk') != -1:
                        try:                        
                            with open('preferences.json') as json_file:
                                data = json.load(json_file)
                                for p in data['VkLogin']:
                                    username = p['user']
                                    password = p['pass']
                        except:
                            msg = 'Insert your VK Username\n'
                            dlg = wx.TextEntryDialog(self, msg, 'VK Login')
                            dlg.CentreOnParent()                
                            if dlg.ShowModal() == wx.ID_OK:  
                                username = dlg.GetValue()                       
                            else:                    
                                return 0     
                            dlg.Destroy()   

                            msg = 'Insert your VK Password\n'
                            dlg = wx.TextEntryDialog(self, msg, 'VK Password')
                            dlg.CentreOnParent()                
                            if dlg.ShowModal() == wx.ID_OK:  
                                password = dlg.GetValue()                       
                            else:                    
                                return 0     
                            dlg.Destroy()    
                            data = {}
                            data['VkLogin'] = []
                            data['VkLogin'].append({
                                'user': username,
                                'pass': password
                            })
                            with open('preferences.json', 'w') as outFile:
                                json.dump(data, outFile)
                        headers = {"Referer": "https://m.vk.com/login?role=fast&to=&s=1&m=1&email="+username
                            , 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0'}
                        # Change email-username and password by your user in VK website
                        payload = {'email': username, 'pass': password}
                        # VK LOGIN COULD BE NECESARY IN CASE THE ACCOUNT BE PRIVATE
                        if payload['email'] == 'EMAIL' or payload['pass'] == 'PASSWORD':
                            string = "Error: Payload Parameters not configured in VK"
                            self.txtResponse.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
                            self.txtResponse.SetValue(string)                       
                            exit(-1)
                        with requests.Session() as S:
                            Loginpage = S.get('https://m.vk.com/login')
                            Loginsoup = BeautifulSoup(Loginpage.content,'lxml')
                            Loginurl = Loginsoup.find('form')['action']
                            p = S.post(Loginurl, data=payload, headers=headers)
                            # NOW YOU ARE SUCCESSFULLY LOGGED IN

                            if "/videos" in url:
                                soup = BeautifulSoup(S.get(url).content, 'html.parser')
                                linkers  = soup.findAll('a', attrs={'class': 'video_item_title', 'href': re.compile("^/video")})
                                string = "Extracting all files into " + directory + " directory."
                                self.txtResponse.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
                                self.txtResponse.SetValue(string)   
                                for linker in list(set(linkers)):
                                    
                                    page = S.get("https://vk.com"+linker.get('href'))
                                    content = page.content
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
                                                cont_file+=1

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
                                            cont_file+=1

                            elif "/photos" in url:

                                soup = BeautifulSoup(S.get(url).content, 'html.parser')
                                linkers = soup.findAll('a', attrs={'href': re.compile("^/photo")})
                                
                                for link in list(set(linkers)):
                                    #print(link.get('href'))
                                    pageFinal = S.get("https://vk.com/"+link.get('href'))                             
                                    soupInner = BeautifulSoup(pageFinal.content, 'html.parser')
                                    linkersInner = soupInner.findAll('img')      
                                    for linkInner in linkersInner:
                                        ext = os.path.splitext((linkInner['src']))[-1].lower()
                                        if ext in listImages and "https://sun9" in linkInner['src']:
                                            
                                            with open(os.path.join("./" + directory + "/photos/", os.path.basename(linkInner['src'])),
                                                        'wb') as f:
                                                response = requests.get(linkInner['src'])
                                                f.write(response.content)                                
                                                cont_file+=1                                        
                                    
                            else:
                                self.txtResponse.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
                                self.txtResponse.SetValue(str('Not valid url for VK'))        
                    # Website not found           
                    else:
                        self.txtResponse.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
                        self.txtResponse.SetValue(str('Not found the website.'))
                    self.txtResponse.SetForegroundColour( wx.Colour(34,139,34) )
                    self.txtResponse.SetValue(str('Downloaded '+ str(cont_file)+ " files."))  
                # User inserted a hispachan url                                             
            else:
                self.txtResponse.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
                self.txtResponse.SetValue(str('Url must start by http or https.'))


    def checkUrl(self, url):    
        if re.match(regex, url) is not None:         
            return True
        else:
            return False
    def createDialog(self):
        msg = 'Select directory Folder\n'
        dlg = wx.TextEntryDialog(self, msg, 'Directory Hierarchy')
        dlg.SetWindowStyleFlag(wx.FRAME_FLOAT_ON_PARENT|wx.DEFAULT_DIALOG_STYLE)
        dlg.CentreOnParent()
        dlg.Show()
        event = 'pass'
        directory = 'default'
        if dlg.ShowModal() == wx.ID_OK:  
            directory = dlg.GetValue()
        else:
            event = "close"
                
        dlg.Destroy()
        return directory, event


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame(parent=None)
    frame.Show()
    app.MainLoop()

