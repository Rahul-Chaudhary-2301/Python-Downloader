import requests
import time
import os, errno
import threading
import urllib.parse
import urllib.request
import shutil
import sys
import console
import tempfile


class Downloader:
    def __init__(self, URL=None, name=None, output_in=None, thread_limit=16):
        self.url = URL
        self.file_name = name
        self.file_size = None
        self.download_path = output_in
        self.__number_of_thread = thread_limit
        self.__url_scheme = None

        if self.url is not None:
            self.grab(self.url, name=self.file_name,download_path = output_in)

        # if self.file_name is None:
        #     self.file_name = os.path.basename(self.url)
        # if self.download_path is None:
        #     self.download_path = os.getcwd()
        # if (self.url and self.file_name and self.download_path) is not None:
        #     self.grab(self.url)

    def get_file_size(URL):
        info = requests.head(URL)
        try:
            file_size = int(info.headers['content-length'])
            return file_size
        except:
            print("Invalid URL")
            return 


    def __FTPHandler(self):
        """
        Method : __FTPHandler(self)

        This Method is used to download the FILE from
        FTP URL Scheme and stores it in a FILE.
        """
        with urllib.request.urlopen(self.url) as response, \
                open(self.file_name, 'wb') as outputFile:
            shutil.copyfileobj(response, outputFile)

    def __HTTPHandler(self, startByte, endByte, thread_number, temp_dir):
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
        # r = requests.get(self.url, headers=headers, stream=True)
        # open the FILE and write the content of the html page
        # into FILE.
        with requests.get(self.url, headers=headers, stream = True) as request:
            with open(temp_dir.name+'/'+str(startByte),'wb') as file:
                shutil.copyfileobj(request.raw, file)

    def __merge_temp_file(self,temp_dir):
        os.chdir(temp_dir.name)
        list_temp_files = os.listdir(temp_dir.name)
        list_temp_files = [int(i) for i in list_temp_files]
        list_temp_files.sort()
        print(list_temp_files)
        file_obj = open(self.download_path+'/'+self.file_name,'w')
        file_obj.write("\0"*self.file_size)
        file_obj.close()
        file_obj = open(self.download_path+'/'+self.file_name,'r+b')

        for file in list_temp_files:
            temp_file_obj = open(str(file),"rb")
            file_obj.seek(file)
            file_obj.write(temp_file_obj.read())
            temp_file_obj.close()
            
        file_obj.close()
        print("File Written")
        time.sleep(1000)
        


                

    def __startFTP(self):
        """Method : __startFTP(self)

        This methods starts the FTP FILE Downloding Process.
        """

        self.__FTPHandler()

    def __startHTTP(self,temp_dir):

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
        self.file_size = Downloader.get_file_size(self.url)
        part = int(self.file_size / self.__number_of_thread)
        

        for i in range(self.__number_of_thread):
            start = part * i
            end = start + part
            # create a Thread with start and end locations
            t = threading.Thread(target=self.__HTTPHandler, kwargs={
                'startByte': start, 'endByte': end, 'thread_number': i, 'temp_dir' : temp_dir})
            
            t.setDaemon(False)   
            t.start()        
            
        t.join()
        del t

        sys.stdout.flush()

    def grab(self, URL, **kwargs):
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

        self.url = URL
        # Getting the name of the file. This option only works for one level of nesting.
        # Changes to the submodule inside of another submodule will not be pushed.
        if (('name' in kwargs.keys() and kwargs['name'])is None) or \
            ('name' not in kwargs.keys()):
            self.file_name = os.path.basename(self.url)
        elif 'name' in kwargs.keys():
            self.file_name = kwargs['name']

        if (('download_path' in kwargs.keys() and kwargs['download_path'])is None) or \
            ('download_path' not in kwargs.keys()):
            self.download_path = os.getcwd()
        else:
            self.download_path = kwargs['download_path']

        
            
        # Getting URL scheme
        self.__url_scheme = urllib.parse.urlparse(URL).scheme

        # Starting Handler
        if self.__url_scheme == 'ftp':
            self.__startFTP()
        elif self.__url_scheme in ['http', 'https']:
            temp_dir = tempfile.TemporaryDirectory()
            print("TEMP : ",temp_dir.name)
            self.__startHTTP(temp_dir)
            self.__merge_temp_file(temp_dir)
            
        else:
            print("URL Scheme is not found")




