import requests
import os, errno
import threading
import urllib.parse
import urllib.request
import shutil
import sys


class Downloader:
    def __init__(self, URL=None, name=None, output_in=None, threadLimit=16):
        self.URL = URL
        self.outputFileName = name
        self.output_in = output_in
        self.number_of_thread = threadLimit
        self.URLScheme = None
        if URL is None:
            return
        if self.outputFileName is None:
            self.outputFileName = os.path.basename(self.URL)
        if self.output_in is None:
            script_working_dir = os.path.dirname(os.path.abspath(__file__))
            output_dir = "{}{}{}{}{}{}{}{}".format(script_working_dir,os.sep,os.pardir,os.sep,os.pardir,os.sep,'downloaded_files',os.sep)
            os.makedirs(output_dir, exist_ok=True)
            self.output_in = output_dir
        print("Saving files in: ", self.output_in)
        self.grab(self.URL, "{}{}".format(self.output_in,self.outputFileName))

    def __FTPHandler(self):
        """
        Method : __FTPHandler(self)

        This Method is used to download the FILE from
        FTP URL Scheme and stores it in a FILE.
        """

        with urllib.request.urlopen(self.URL) as response, \
                open(self.outputFileName, 'wb') as outputFile:
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
        r = requests.get(self.URL, headers=headers, stream=True)

        # open the FILE and write the content of the html page
        # into FILE.
        fp = open(self.outputFileName, "r+b")
        fp.seek(int(startByte))
        sys.stdout.write("File Written by " + str(thread_number) + "\r")
        fp.write(r.content)

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
            file_size = int(info.headers['content-length'])
        except:
            print("Invalid URL")
            return
        part = int(file_size / self.number_of_thread)
        file = open(self.outputFileName, "wb")
        file.write('\0'.encode() * file_size)
        file.close()
        # Creating folder to store part file
        for i in range(self.number_of_thread):
            start = part * i
            end = start + part
            sys.stdout.write("Thread " + str(i) + " Started. \r")
            # create a Thread with start and end locations
            t = threading.Thread(target=self.__HTTPHandler, kwargs={
                'startByte': start, 'endByte': end, 'thread_number': i})
            t.setDaemon(False)
            t.start()
        t.join()
        del t
        return

    def grab(self, URL, name=None):
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

        self.URL = URL
        # Getting the name of the file. This option only works for one level of nesting.
        # Changes to the submodule inside of another submodule will not be pushed.
        if name is None:
            if self.outputFileName == None:
                self.outputFileName = os.path.basename(self.URL)
        else:
            self.outputFileName = name
        # Getting URL scheme
        if self.URLScheme is None:
            self.URLScheme = urllib.parse.urlparse(URL).scheme
        # Starting Handler
        if self.URLScheme == 'ftp':
            self.__startFTP()
        elif self.URLScheme in ['http', 'https']:
            self.__startHTTP()
        else:
            print("URL Scheme is not found")
        exit()
