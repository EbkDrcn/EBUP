import time
import socket

def msgIdGenerator():
    '''
    ID generator for chunked messages. Creates a 4 digit message id.
    '''
    randomNumber = time.time()
    msgID = str(randomNumber).split('.')[-1][-4:]
    return msgID

def getLocalIP():
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
    for ip in answers:
        if not any(item["ipAddress"] == ip for item in protocol.addressBook) and ip != protocol.systemID:
            protocol.addressBook.append({"ipAddress":ip, "createdTime":time.time()})

    return protocol.addressBook

def packetValidator(protocol, packet):
    if isinstance(packet, list) and len(packet) == 5:
        if packet[0] == protocol.starterBit and packet[-1] == protocol.enderBit:
            return True
    else:
        return False