import requests
import os
import threading
from urllib import requests as req
from hurry.filesize import size

class Downloader:
    def __init__(self, fileURL = None, name = None):
        self.fileURL = fileURL
        self.name = name
        if self.name == None:
            self.name = os.path.basename(self.fileURL)
        self.threadlimit = None

    def __DownloadFTP():
        pass

    def __GetThreadCount(filesize):
        if filesize 

    def __HTTPhandler(self, fileName, startByte, endByte):
        headers = {'Range': 'bytes=%d-%d' % (start, end)} 
  
        # request the specified part and get into variable     
        r = requests.get(url, headers=headers, stream=True) 
      
        # open the file and write the content of the html page  
        # into file. 
        with open(filename, "r+b") as fp: 
            fp.seek(int(start)) 
            
            fp.write(r.content)

    def grab(self,fileURL, name=None)
        if self.name == None:
            self.name = os.path.basename(self.fileURL)
        

    def __UI():
        pass

    def __ProgressBar():
        pass

    def __MultiThread():
        pass

    def FileDetail():
        pass

    def __Pause():
        pass

    def __Resume():
        pass
    
    
    
        
