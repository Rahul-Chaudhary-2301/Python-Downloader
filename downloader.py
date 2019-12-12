import requests
import os, errno
import threading
import urllib.parse
import urllib.request
import shutil
import sys
import console



class Downloader:
    def __init__(self, URL=None, name=None, output_in=None, threadLimit=16):
        self.URL = URL
        self.FileName = name
        self.FileSize = None
        self.FileDir = output_in
        self.FileDownloaded = False
        self.number_of_thread = threadLimit
        self.URLScheme = None
        self.TerminalSize = shutil.get_terminal_size()
        self.DownloadStartTime = None
        self.DownloadStarted = False

        if URL is None:
            return
        if self.FileName is None:
            self.FileName = os.path.basename(self.URL)
        if self.FileDir is None:
            script_working_dir = os.path.dirname(os.path.abspath(__file__))
            output_dir = "{}{}{}{}{}{}{}{}".format(script_working_dir,os.sep,os.pardir,os.sep,os.pardir,os.sep,'downloaded_files',os.sep)
            os.makedirs(output_dir, exist_ok=True)
            self.FileDir = output_dir
        print("Saving files in: ", self.FileDir)
        if (self.URL and self.FileName and self.FileDir) is not None:
            self.grab(self.URL)

    def __FTPHandler(self):
        """
        Method : __FTPHandler(self)

        This Method is used to download the FILE from
        FTP URL Scheme and stores it in a FILE.
        """

        with urllib.request.urlopen(self.URL) as response, \
                open(self.FileName, 'wb') as outputFile:
            shutil.copyfileobj(response, outputFile)

    def __HTTPHandler(self, startByte, endByte, thread_number):
        """
        Method : __HTTPHandler(self, fileName, startByte, endByte)

        Parameters :
        fileName  : It is name of the FILE where the
        downloaded data will store.
        startByte : It is a used to set the pointer
        from which the data will start
        downloading.
        endByte   : It is a pointer till there the
        data will be downloaded.
        thread_number   : It is the number of thread
        This Method is used to download the specific range of bytes
        which is passed and store the data in .part-{thread_number}
        FILE.
        """

        headers = {'Range': 'bytes=%d-%d' % (startByte, endByte)}

        # request the specified part and get into variable
        # r = requests.get(self.URL, headers=headers, stream=True)
        # open the FILE and write the content of the html page
        # into FILE.
        # with open(self.FilePath, "r+b") as file:
        #     file.seek(int(startByte))
        #     print("Thread Number : {}  - startByte : {}".format(thread_number,startByte))
        #     file.write(r.content)
        #     file.close()
        with requests.get(self.URL, headers=headers, stream = True) as request:
            with open(self.FileDir+'/'+str(startByte),'wb') as file:
                shutil.copyfileobj(request.raw, file)
                # print("FileName {} \t| FileSize {}".format(self.FileDir+'/'+str(startByte),os.path.getsize(self.FileDir+'/'+str(startByte))))


    # def __DisplayStatus(self):
    #     while self.FileDownloaded is not True:
    #         sys.stdout.write(" "*(self.TerminalSize.columns - 21) + "Time Escaped : {}\r".format())
    #         sys.stdout.write("{}  : {}     | Size : {}\r".format(self.FileName,self.FileSize))
    def __Display(self):
        while self.DownloadStarted is True:
            # if  self.FileDownloaded is not True:
            #     FileList = os.listdir(self.FileDir)
            #     sum = 0
            #     print(FileList)
            #     for file in FileList:
            #         try:
            #             filesize = os.path.getsize(self.FileDir+'/'+file)
            #             sum += filesize
            #         except FileNotFoundError:
            #             print("FileNotFoundError")
            #     try:
                    
            #         percentage = (filesize/self.FileSize) * 100
            #         sys.stdout.write("\t|Percentage : {} \n".format(str(percentage)))
            #     except:
            #         sys.stdout.write("ERROR ECCOURED\r")
            print("A")


    def __startFTP(self):
        """Method : __startFTP(self)

        This methods starts the FTP FILE Downloding Process.
        """

        self.__FTPHandler()

    def __startHTTP(self):

        """
        Method: __startHTTP(self)

        This method starts File Downloading Process of HTTP Scheme.
        The following steps explains the execution of the method:

        Step1: Gets the header data of the URL
        Step2: Gets the File Size from Header
        Step3: Divide the FILE Size from number_of_threads
        The part is the total total bytes which 1 thread
        will download
        Step4: Creates a output file of total file size.
            Note: 'This is done because of multi threading purpose'
        Step5: Start multithreading
        Step6: Join all threads
        """

        info = requests.head(self.URL)
        try:
            self.FileSize = int(info.headers['content-length'])
        except:
            print("Invalid URL")
            return

        part = int(self.FileSize / self.number_of_thread)
        self.FilePath = self.FileDir +os.sep +self.FileName
        # file = open(self.FilePath , "wb")
        # file.write('\0'.encode() * self.FileSize)
        # file.close()
        sys.stdout.write("URL : {} \n".format(self.URL))
        # sys.stdout.write("\tDownloading : {} [Size : {}]\r".format(self.FileName,self.FileSize))
        
        for i in range(self.number_of_thread):
            start = part * i
            end = start + part
            # sys.stdout.write("Thread " + str(i) + " Started. \r")
            # create a Thread with start and end locations
            t = threading.Thread(target=self.__HTTPHandler, kwargs={
                'startByte': start, 'endByte': end, 'thread_number': i})
            
            t.setDaemon(False)   
            t.start()        
            
        
        # for th in threading.enumerate():
        #     if th.daemon:
        #         th.join()
        self.FileDownloaded = True
        self.DownloadStarted = False
        t.join()
        del t
        # s.join()
        # del s
        sys.stdout.flush()
        
        # sys.stdout.write("Downloaded : {}\n".format(self.FileName))

    def grab(self, URL=None, name=None):
        """
        Method : grab(self, URL, name = None)

        Parameter :
        URL : The URL of the FILE to download.
        [name = None] : It is an optional parameter
        to specify custom name to download file
        This Methods gets the requried data for downloading
        the FILE. IT calls the start methods where actually
        FILE Downloading starts.
        """
        if self.URL is None:
            self.URL = URL
        # Getting the name of the file. This option only works for one level of nesting.
        # Changes to the submodule inside of another submodule will not be pushed.
        if name is None:
            if self.FileName is None:
                self.FileName = os.path.basename(self.URL)
        else:
            self.FileName = name
        # Getting URL scheme
        self.URLScheme = urllib.parse.urlparse(URL).scheme
        # Starting Handler
        if self.URLScheme == 'ftp':
            self.__startFTP()
        elif self.URLScheme in ['http', 'https']:
            # e = Event()
            # self.DownloadStarted = True
            # p2 = Process(target = self.__Display)
            # p2.start()
            # p1 = Process(target = self.__startHTTP)
            # p1.start()
            
            # e.set()
            # p2.join()
            # p1.join()
            self.__startHTTP()
            
        else:
            print("URL Scheme is not found")
