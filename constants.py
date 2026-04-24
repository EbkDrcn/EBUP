class EBUPConstants:
    ackQuery = {"type":"ack_query", "data":"ack_check"}
    ackAffirmative = {"type":"ack_query", "data":"ack_affirmative"}
    ackNegative = {"type":"ack_query", "data":"ack_negative"}
    msgRecieved = {"type":"msgInfo", "data":"msg_recieved"}
    msgTypeError = {"type":"msgInfo", "data":"msg_returned_type_error"}
    discoverySearch = {"type":"discovery", "data":"discovery"}
    discoveryAns = {"type":"discovery", "data":"discovery_here"}
    versionCheck = {"type":"discovery", "data":"versionCheck"}
    message = {"type":"msg", "data":"", "priority":False}

    defaultPort = 1302
    starterBit = "EBUP-S-v1"
    enderBit = "EBUP-E-v1"
    version = 1