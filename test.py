from downloader import Downloader
import threading
import sys
import os
# url ="https://icatcare.org/app/uploads/2018/07/Thinking-of-getting-a-cat.png"
# url = "https://www.freepngimg.com/thumb/cool_effects/11-2-cool-effects-png-picture.png"
# url = "https://www.wikihow.com/images/thumb/c/c8/Do-a-Tempo-Run-Step-1.jpg/aid11414242-v4-900px-Do-a-Tempo-Run-Step-1.jpg"
url = "http://ftp.debian.org/debian/pool/main/0/0ad-data/0ad-data-common_0.0.17-1_all.deb"
# url = "http://ftp.debian.org/debian/pool/main/a/android-platform-development/android-platform-development_7.0.0+r33.orig.tar.xz"
alive = True

def start_downloading():
    print("Testing Downloading")
    

    obj = Downloader(URL=url, name="pkg.deb")
def print_A():

    while alive:
        FileDir = "/home/rahul/downloaded_files"
        FileList = os.listdir(FileDir)
        sum = 0
        #print(FileList)
        for file in FileList:
            try:
                filesize = os.path.getsize(FileDir+'/'+file)
                sum += filesize
            except FileNotFoundError:
                print("FileNotFoundError")
        try:
            
            percentage = int((sum/776704) * 100)
            sys.stdout.write("\t|Percentage : {} \r".format(str(percentage)))
        except:
            sys.stdout.write("ERROR ECCOURED\r")

if __name__ == "__main__":
    t = threading.Thread(target=start_downloading)
    t.start()
    a = threading.Thread(target=print_A)
    a.setDaemon(True)
    a.start()
    t.join()
    alive = t.isAlive()
    a.join()