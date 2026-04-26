import time
import socket
import json
from math import ceil

def msgIdGenerator():
    '''
    ID generator for chunked messages. Creates a 4 digit message id.
    '''
    randomNumber = time.time()
    msgID = str(randomNumber).split('.')[-1][-4:]
    return msgID

def getLocalIP():
    '''
    Gets clients IP address. If not gets local address
    '''
    ipGetter = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        ipGetter.connect(("8.8.8.8", 80))
        ip = ipGetter.getsockname()[0]
        
    except Exception:
        ip = "127.0.0.1"
    
    finally:
        ipGetter.close()

    return ip

def updateAddressBook(protocol, answers):
    '''
    Updates clients address book with answers list given as parameter.
    '''
    for ip in answers:
        if not any(item["ipAddress"] == ip for item in protocol.addressBook) and ip != protocol.systemID:
            protocol.addressBook.append({"ipAddress":ip, "createdTime":time.time()})

    return protocol.addressBook

def packetValidator(protocol, packet):
    '''
    Validates given packet if it's a EBUP packet or not.
    '''
    if isinstance(packet, list) and len(packet) == 5:
        if packet[0] == protocol.starterBit and packet[-1] == protocol.enderBit:
            return True
    else:
        return False

def splitData(data):
    msgID = msgIdGenerator()
    data = data.encode("utf-8")
    chunkedData = []
    totalChunk = ceil(len(data)/1024)

    for i in range(0,len(data), 1024):
        chunk = data[i:i+1024]
        chunkedData.append(chunk)

    return chunkedData, totalChunk, msgID
