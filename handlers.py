ackQuery = {"type":"ack_query", "data":"ack_check"}
ackAffirmative = {"type":"ack_query", "data":"ack_affirmative"}
msgRecieved = {"type":"msgInfo", "data":"msg_recieved"}
msgTypeError = {"type":"msgInfo", "data":"msg_returned_type_error"}
discoverySearch = {"type":"discovery", "data":"discovery"}
discoveryAns = {"type":"discovery", "data":"discovery_here"}
versionCheck = {"type":"remoteInfo", "data":"versionCheck"}
message = {"type":"msg", "data":"", "priority":False}

def handleMsg(protocol, senderID, payload):
    print(f"\n [!] Mesaj alındı. Kaynak : {senderID}")
    print(f"İçerik : {payload.get("data")} \n")
    if payload.get("priority") == True:
        self.sendPocket(senderID, self.msgRecieved)

def handleDiscovery(protocol, senderID, payload):
    if payload == self.discoverySearch:
        self.sendPocket(senderID, self.discoveryAns)
        print(f"Discovery search from {senderID} , answered.")
    elif payload == discoveryAns:
        self.buffer.append(f"DISCOVERY_ANS_FROM_{senderID}")
        print(f"Discovery answer from {senderID}")
    