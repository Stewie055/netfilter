
if packet.haslayer(TCP):
    # Use a filter to select TCP packete.
    # For example : if packet[TCP].dport == 80


    # recalculate length and checksum
    packet[IP].len = len(str(packet))
    packet[TCP].len = len(str(packet[TCP]))
    del packet[IP].chksum,packet[TCP].chksum
    # send packet modifed
    payload.set_verdict_modified(nfqueue.NF_ACCEPT, str(packet), len(packet))#set the packet content to our modified version

