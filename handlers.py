def handleMsg(protocol, senderID, payload):
    print(f"\n [!] Mesaj alındı. Kaynak : {senderID}")
    print(f"İçerik : {payload.get('data')} \n")
    if payload.get("priority") == True:
        protocol.sendPocket(senderID, protocol.msgRecieved)

def handleDiscovery(protocol, senderID, payload):
    if payload == protocol.discoverySearch:
        protocol.sendPocket(senderID, protocol.discoveryAns)
        print(f"Discovery search from {senderID} , answered.")
    elif payload == protocol.discoveryAns:
        protocol.buffer.append(f"DISCOVERY_ANS_FROM_{senderID}")
        print(f"Discovery answer from {senderID}")
    elif payload == protocol.versionCheck:
        versionResponse = {"type":"discovery", "version":protocol.version}
        protocol.sendPocket(senderID, versionResponse)
    elif payload.get("version") :
        print(f"Remote machine is running on EBUP version {payload.get('version')}")    

def handleMsgInfo(protocol, senderID, payload):
    if payload == protocol.msgRecieved:
        print(f"Your priority message to {senderID} is sended")
    elif payload == protocol.msgTypeError:
        print(f"Your last message to {senderID} retuned a type error")

def handleAckQuery(protocol, senderID, payload):
    if payload == protocol.ackQuery:
        if protocol.doNotDisturb == False:
            protocol.sendPocket(senderID, protocol.ackAffirmative)
            print(f"{senderID} system checked if you are available, response given as available")
        else:
            protocol.sendPocket(senderID, protocol.ackNegative)

    elif payload == protocol.ackAffirmative:
        protocol.buffer.append(f"ACK_RESPONSE_POSITIVE_{senderID}")
    elif payload == protocol.ackNegative:
        protocol.buffer.append(f"ACK_RESPONSE_NEGATIVE_{senderID}")
