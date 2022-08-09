
import urllib
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import urllib.robotparser
import asyncio
import socket
import pyppeteer
import asyncio


class Browser():
    def __init__(self, url):
        self.url = url
        self.links = []
        
        self.parsed_url = urllib.parse.urlparse(url)
        self.naming = self.parsed_url.netloc.replace(".", "-")
        self.mobil = {
            'width': 375,
            'height': 667  
        }
        self.tablet = {
            'width': 810,
            'height': 1080  
        }
        self.desktop = {
            'width': 1280,
            'height': 1024  
        }
        self.currentIP = socket.gethostbyname(self.parsed_url.netloc)



    async def intercept_network_request(self,request, url):
        request.__setattr__('_allowInterception', True)
        if request.url.startswith('http'):
           
            parsed_url = urllib.parse.urlparse(request.url)
            ip = socket.gethostbyname(parsed_url.netloc)
            if self.currentIP  !=  ip and request.url not in  self.requests_url:
                self.requests_url.append(request.url)
               
     
        return await request.continue_()
        
      


    async def open_browser(self, url):
        
        self.browser = await pyppeteer.launch(executablePath='/usr/bin/google-chrome-stable',headless=True, args=['--no-sandbox'])
        self.page = await self.browser.newPage()
        
        #await self.page.setRequestInterception(True)
        page = await self.open_page(url)
        
       
        return page

    async def open_page(self, url):
        page = {}
        self.requests_url = []
        requests = self.page.on('request', lambda req: asyncio.ensure_future(self.intercept_network_request(req, url)))
        await self.page.goto(url,{
         'waitUntil': 'load',
         'timeout': 25000,
        })
        
        page['content'] = await self.page.content()
        page['cookies'] = await self.page.cookies()
        page['screenshots'] = await self.page.cookies()
        page['requests'] =self.requests_url

     #   await self.page.setViewport(self.mobil)
      #  await self.page.screenshot({'path': 'mobil.png'})
     #   await self.page.setViewport(self.tablet)
     #   await self.page.screenshot({'path': 'tablet.png'})
     #   await self.page.setViewport(self.desktop)
     #   await self.page.screenshot({'path': 'desktop.png'})    
        return page       


