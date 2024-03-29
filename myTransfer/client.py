# ! /usr/bin/env python3

# Echo client program
import socket, sys, re, os
from os import listdir
from os.path import isfile, join

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive

askProxy = input('Would you like to use a stammer proxy?(y/n)')

if 'y' in askProxy:
    port = '50000'
else:
    port = '50001'

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:"+port),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "fileTransferClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)
print([f for f in listdir(os.getcwd())])
command = ""
while not command:
    command = input("Enter a file name or change a directory: ")
    args = command.split()
    if args[0] == "cd":
        dir = ""
        newdir = ""
        dir = os.getcwd()
        dir = dir.split("/")
        if(args[1] == ".."):
            for i in range(len(dir)-1):
                newdir += dir[i]
                if i != len(dir)-2:
                    newdir += "/"
        else:
            newdir = args[1]
        os.chdir(newdir)
        onlyfiles = [f for f in listdir(os.getcwd())]
        print(onlyfiles)
        command = ""

    try:
        inputFile = open(command, "r")
    except FileNotFoundError:
        print("File Not Found Error")
        command = ""

    inputText = inputFile.read()
    if not inputText:
        print("File is empty. Please use a file with contents.")
        command = ""

#View #1 on Collaboration Report
inputText = inputText.replace("\n", "@")
inputFile.close()

print("sending " + command)
framedSend(s, inputText.encode(), debug)
print("received:", framedReceive(s, debug))
