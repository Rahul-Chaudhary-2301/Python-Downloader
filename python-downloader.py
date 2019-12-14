from downloader import Downloader
from datetime import timedelta
from colorama import Fore, Style
from stopwatch import Stopwatch
import threading
import time
import sys
import os

class PyDownloader:
    def __init__(self,URL,name):
        self.URL = URL
        self.name = name
        self.__alive = None
        self.file_dir =  "/home/rahul/downloaded_files"
        self.__sw = Stopwatch()
        self.file_size = 0
        self.__curr_file_size = -1
    def start_downloading(self):
        self.file_size = Downloader.get_file_size(self.URL)
        self.__sw.start()
        obj = Downloader(self.URL,self.name)

    def file_merging(self):
        pass

    def display(self):
        print("GET : ",self.URL)
        print("Downloading : ",self.name)
        print("FILE SIZE : ",self.file_size)
        bar_length = 70
        
        while self.curr_file_size <= self.file_size:
            time.sleep(0.2)
            file_list = os.listdir(self.file_dir)
            curr_total_size = 0
            for file in file_list:
                try:
                    file_size = os.path.getsize(self.file_dir+'/'+file)
                    self.__curr_file_size += file_size
                except FileNotFoundError:
                    print("FileNotFoundError")
            try:
                percentage = int((self.__curr_file_size /self.file_size) * 100)
                filled_bar = int((bar_length/100)*percentage)
                if filled_bar > 100:
                    filled_bar = 100
                sys.stdout.write("Percentage : {} |{}{}{}{}| |Time Escaped : {}\r".format(
                    str(percentage),
                    Fore.RED,
                    '#'*filled_bar,
                    Style.RESET_ALL,
                    ' '*(bar_length-filled_bar),
                    str(str(timedelta(seconds=int(self.__sw.duration))))))
            except ZeroDivisionError:
                # sys.stdout.write("ERROR ECCOURED\r")
                pass


        sys.stdout.write("\n"*2)
        print("CURR :",self.__curr_file_size )
        self.sw.stop()
            
    def main(self):
        t = threading.Thread(target=self.start_downloading)
        t.start()
        self.alive = t.isAlive()
        a = threading.Thread(target=self.display)
        a.setDaemon(False)
        a.start()
        t.join()
        self.alive = t.isAlive()
        a.join()

url = "http://ftp.debian.org/debian/pool/main/0/0ad-data/0ad-data-common_0.0.17-1_all.deb"

obj = PyDownloader(URL=url,name="pkg.deb")
obj.main()
