import socket
import json
import threading

starterBit = "STARTERBIT/WELCOMETOEBUBITSCOMM"
enderBit = "ENDERBIT/GOODBYEFROMEBUBITSCOMM"

class ebuBits :
    defaultPort = 1302

    def __init__(self, systemID, systemPort = defaultPort):
        self.systemID = systemID
        self.systemPort = systemPort
        self.buffer = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            self.socket.bind(('127.0.0.1', self.systemPort))
            print(f"Sistem {systemID} established. Port {self.systemPort}")
        except OSError:
            print(f"Error establishing port {self.systemPort}, already in use")

        self.running = True
        self.listenerThread = threading.Thread(target=self.listenForever, daemon=True)
        self.listenerThread.start()

    def sendPocket(self, destination,  data):
        packet = starterBit + self.systemID + destination + data + enderBit
        jsonPacket = json.dumps(packet).encode("utf-8")

        self.socket.sendto(jsonPacket, ('127.0.0.1', self.systemPort))

    def listenForever(self):
        while self.running:
            try:
                raw_data, addr = self.socket.recvfrom(4096)
                packet = json.loads(raw_data.decode("utf-8"))

                self.parsePacket(packet)

            except Exception as e:
                pass

    def parsePacket(self, packet):
        if packet[:4] == starterBit:
            senderID = packet[4]
            destinationID = packet[5]
            payload = packet[6]

            if packet[-4:] == enderBit:
                if destinationID == self.systemID:
                    print(f"\n [!] Mesaj alındı. Kaynak : {senderID}")
                    print(f"İçerik : {payload} \n")

                else:
                    print(f"Başkasına gönderilen bir mesaj bulundu")





