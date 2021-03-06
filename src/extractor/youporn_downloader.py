from __future__ import division, print_function, unicode_literals
import downloader
import ree as re
from io import BytesIO
import os
from constants import try_n
from utils import Downloader, LazyUrl, get_ext, format_filename, clean_title
import youtube_dl



@Downloader.register
class Downloader_youporn(Downloader):
    type = 'youporn'
    single = True
    URLS = ['youporn.com']
    
    def init(self):
        if self.url.startswith('youporn_'):
            self.url = 'https://www.youporn.com/watch/{}'.format(self.url.replace('youporn_', '', 1))

    def read(self):
        video = Video(self.url)

        self.urls.append(video.url)
        self.setIcon(video.thumb)

        self.customWidget.enableSegment()

        self.title = video.title


class Video(object):
    @try_n(4)
    def __init__(self, url):
        ydl = youtube_dl.YoutubeDL()
        info = ydl.extract_info(url)

        f = info['formats'][-1]
        url_video = f['url']
        self.url = LazyUrl(url, lambda _: url_video, self)
        
        self.url_thumb = info['thumbnails'][0]['url']
        self.thumb = BytesIO()
        downloader.download(self.url_thumb, buffer=self.thumb)
        self.title = info['title']
        ext = get_ext(url_video)
        self.filename = format_filename(self.title, info['id'], ext)
