import socket
import json
import threading
import time

import handlers
from constants import EBUPConstants
import utils

class EBUProtocol(EBUPConstants) :
    doNotDisturb = False
    defaultPort = EBUPConstants.defaultPort
    
    addressBook = []

    def __init__(self, systemID = None, systemPort = defaultPort):
        if systemID is None:
            systemID = utils.getLocalIP()
            self.systemID = systemID
        else:
            self.systemID = systemID
            
        self.systemPort = systemPort

        print(f"EBUP interface initialized. Your system ID is {self.systemID} and your port is {self.systemPort}")
        
        self.buffer = []
        self.chunkBuffer = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SOL_BROADCAST, 1)
        self.setAddressBook = True

        try:
            self.socket.bind(('0.0.0.0', self.systemPort))
            print(f"System {systemID} established. Port {self.systemPort}")
        except OSError:
            print(f"Error establishing port {self.systemPort}, already in use")

        self.running = True
        self.listenerThread = threading.Thread(target=self.listenForever, daemon=True)
        self.listenerThread.start()

        self.handlers = {
            "msg" : handlers.handleMsg,
            "discovery" : handlers.handleDiscovery,
            "ack_query" : handlers.handleAckQuery,
            "msgInfo" : handlers.handleMsgInfo
        }

    def sendPocket(self, destination,  data, priority = False):
        if not isinstance(data,dict):
            if not isinstance(data, str):
                data = str(data)
            data = {"type":"msg", "data":data}
        
        if priority == True:
            data["priority"] = True

        if not data.get("type") == "chunk" and len(data["data"].encode("utf-8")) > 1024:
            self.sendChunk(destination, data["data"])
            return

        packet = [  self.starterBit,
                    self.systemID,
                    destination,
                    data,
                    self.enderBit]

        self.sendJson(packet)

    def listenForever(self):
        while self.running:
            try:
                raw_data, addr = self.socket.recvfrom(4096)
                packet = json.loads(raw_data.decode("utf-8"))

                self.parsePacket(packet)

            except Exception as e:
                pass

    def parsePacket(self, packet):
        if not utils.packetValidator(self, packet):
            return

        senderID = packet[1]
        destinationID = packet[2]
        payload = packet[3]

        if destinationID == self.systemID:
            payloadType = payload.get("type")
            handler = self.handlers.get(payloadType)

            if handler:
                handler(self ,senderID, payload)
            else:
                print(f"Unknown message type received. Message type : {payloadType}")
                self.sendPocket(senderID, self.msgTypeError)
        else :
            print("There is a message for somebody else on the network")

    def isAvailable(self, destination, timeout = 3):
        self.sendPocket(destination, self.ackQuery)
        ackTimer = time.time()
        echoTimer = time.perf_counter()

        expectedACK = f"ACK_RESPONSE_POSITIVE_{destination}"
        negativeACK = f"ACK_RESPONSE_NEGATIVE_{destination}"

        while time.time() - ackTimer < timeout :
            if expectedACK in self.buffer:
                latency = (time.perf_counter() - echoTimer)*1000
                print(f"{destination} system is available. Latency -> {latency:.2f} ms")
                self.buffer.remove(expectedACK)
                return True
            elif negativeACK in self.buffer:
                latency = (time.perf_counter() - echoTimer)*1000
                print(f"{destination} system is not available. Latency -> {latency:.2f} ms")
                self.buffer.remove(negativeACK)
                return False
            time.sleep(0.1)
        print(f"Request to system {destination} timed out")
        return False

    def discovery(self, timeout):
        self.sendPocket("255.255.255.255", self.discoverySearch)
        discoveryTimer = time.time()
        expectedDiscovery = "DISCOVERY_ANS_FROM_"
        print(f"Discovery call for {timeout} seconds.")

        answers = []
        
        while time.time() - discoveryTimer < timeout:
            for item in list(self.buffer):
                if isinstance(item, str) and item.startswith(expectedDiscovery):
                    foundIP = item.replace(expectedDiscovery, "")

                    if foundIP not in answers and foundIP != self.systemID:
                        answers.append(foundIP)
                        print(f"System {foundIP} answered")

                    self.buffer.remove(item)
            time.sleep(0.1)

        if not answers:
            print(f"There is no answer to discovery call")
        else:
            print(f"There is {len(answers)} answers and from {answers}")
        
        if self.setAddressBook == True:
            utils.updateAddressBook(answers)
        else:
            self.addressBook = []

        return answers

    def sendChunk(self, destination, data):
        data, totalChunks, msgID = utils.splitData(data)

        for i in range(0,totalChunks):
            payload = self.chunkedMessage.copy()
            payload["msgID"] = msgID
            payload["total"] = totalChunks
            payload["index"] = i
            payload["data"] = data[i]

            packet = [  self.starterBit,
                        self.systemID,
                        destination,
                        payload,
                        self.enderBit]

            self.sendJson(packet)
            time.sleep(0.1)

    def sendJson(self, packet):
        destination = packet[2]
        jsonPacket = json.dumps(packet).encode("utf-8")
        try:
            self.socket.sendto(jsonPacket, (destination, self.systemPort))

        except Exception as e:
            print(f"Error : {e}")

    
