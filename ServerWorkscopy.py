from Tkinter import *
import sys
import datetime
import time
import hashlib
import os
import select
import threading
import mimetypes
import Tkinter, Tkconstants, tkFileDialog
#from socket import *
import socket
#host = ""
#port = 8080
#buf = 1024
#addr = (host, port)
#UDPSock = socket(AF_INET, SOCK_DGRAM)

#port2 = 8081
#addr2 = (host, port2)
#UDPSock2 = socket(AF_INET, SOCK_DGRAM)

#UDPSock.bind(addr)
i = 1
key = 1
def toChar(x):
  return chr(x + 96)
def toNum(x):
  return ord(x) - 96


def fiveMinuteTimer():
 global key
 while True:
     sum = 0
     now = datetime.datetime.now()
     while True:
         time.sleep(0.1)
         nows = datetime.datetime.now()
         if nows - now > datetime.timedelta(seconds = 3):#minutes = 5):
             print now
             print datetime.datetime.now()
             strw = "okay"
             result = hashlib.md5(strw.encode())
             print ("The hexadecimal equivalent of hash is : ")
             word = result.hexdigest()
             for i in word[0:4]:
                 print i
                 sum = sum + int(i, 16)
             print sum
             key = (sum % 25) + 1
             return key

def bclicked(event = None):
    encrypt()

def oneSecondsTimer():
    while True:
        now = datetime.datetime.now()
        while True:
            time.sleep(0.1)
            nows = datetime.datetime.now()
            if nows - now > datetime.timedelta(seconds = 1):
                decrypt()


def setup(event = None):
    t = threading.Thread(target = fiveMinuteTimer)
    m = threading.Thread(target = decrypt)
    mf = threading.Thread(target = decryptFile)
    mf.daemon = 1  # Kill the child if the parent ends
    m.daemon = 1  # Kill the child if the parent ends
    t.daemon = 1  # Kill the child if the parent ends
    mf.start()
    m.start()
    t.start()

def encrypt():
     PrintMessage['text'] = PrintMessage['text'] + e1.get() + '\n'
     word = list(e1.get())
     data1 = "".join(word)
     for letter in range(0,len(word)):
         word[letter] = word[letter].lower()
         if key + toNum(word[letter]) > 26:
                 temp = abs(toNum(word[letter]) +(key) - 26) #toNum(word[letter])
                 word[letter] = toChar( int(temp)) #toNum(word[letter]) +
         elif toNum(word[letter]) > 0 and toNum(word[letter]) <= 26:
             word[letter] = toChar(toNum(word[letter]) + int(key))
         else:
             continue
     encrypted_words = "".join(word)
     userNumber['text'] = encrypted_words#e1.get()
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s.connect(("localhost",8181))
     s.send(encrypted_words)
     s.close()
     #UDPSock2.sendto(encrypted_words, addr2)
def encryptFile(event = None):

    filename = tkFileDialog.askopenfilename(initialdir = "/",
                                            title = "Select file"
                                            )

    # bytes_read = open(filename, "rb").read()
    # bytes_read = "".join(map(lambda a: chr((ord(a) + 5) % 256) , bytes_read ))

    file = open(filename, "rb")
    bytes_read = file.read()
    print os.path.splitext(file.name)[-1]
    ex = "file:" + str(os.path.splitext(file.name)[-1])
    bytes_read = "".join(map(lambda a: chr((ord(a) + 5) % 256),bytes_read)) + ex


    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect(("localhost",8188))
    #while (data):
    s2.send(bytes_read)
      #l = myarray.read(1024)
    s2.close()
    print("Sent file")

def decryptFile():
  global i
  s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print "bind to 8182"
  s2.bind(("localhost",8182))
  s2.listen(1)
  while True:
    sc, address = s2.accept()
    l = sc.recv(1024)
    data = l
    while(l):
      l = sc.recv(1024)
      data += l
    # print data
    sc.close()
    extention = data.split("file:")[1]
    data = data.split("file:")[0]
    data = "".join(map(lambda a: chr((ord(a) - 5) % 256) , data ))
    # print mimetypes.guess_type(data)
    # print(os.path.splitext(write(data)))
    with open(time.ctime() + extention, 'wb') as f:
        f.write(data)
    print("wrote file")
    # PrintMessage['text'] = 'File received'



def decrypt():
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "bind to 8180"
    s2.bind(("localhost",8180))
    s2.listen(1)
    while True:
      sc, address = s2.accept()

      shift = 26 - key
      l = sc.recv(1024)
      data = l
      while(l):
        l = sc.recv(1024)
        data += l
      sc.close()
      #(data, addr) = UDPSock.recvfrom(buf)
      word = list(data)
      #print(word)
      for letter in range(0,len(word)):
          word[letter] = word[letter].lower()
          if shift + toNum(word[letter]) > 26:
                  temp = abs(toNum(word[letter]) +(shift) - 26) #toNum(word[letter])
                  word[letter] = toChar( int(temp)) #toNum(word[letter]) +
          elif toNum(word[letter]) > 0 and toNum(word[letter]) <= 26:
              word[letter] = toChar(toNum(word[letter]) + int(shift))
          else:
              continue
      word = "".join(word)
      print(word)
      PrintMessage['text'] = PrintMessage['text'] + word + '\n'

master = Tk()
master.title("server")
setup()

output = Label(master,text = "")
output.grid(column = 0, row = 1, columnspan = 1)

userNumber = Label(master,text = "")
userNumber.grid(column = 3, row = 1, columnspan = 5)

e1 = Entry(master)
e1.grid(row=6, column=0, columnspan = 1)

sendButton = Button(master, text="Send")
sendButton.grid(column = 1, row = 6, columnspan = 5)
sendButton.bind("<Button>", bclicked)


sendButtonf = Button(master, text="Send File")
sendButtonf.grid(column = 1, row = 7, columnspan = 5)
sendButtonf.bind("<Button>", encryptFile)


PrintMessage = Label(master,text = "")
PrintMessage.grid(column = 0, row = 1, columnspan = 5)

#decrypt()

mainloop()
