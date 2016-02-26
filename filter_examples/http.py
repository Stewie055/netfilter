
if packet.haslayer(TCP):
    # HTTP packate through port 80
    # dport is the destination port, sport is the source port
    if packet[TCP].dport == 80 and packet.haslayer(Raw):
        if debug:
            print packet.summary()
            print "*" * 10 + "Package load before " + "*" * 10
            print packet[Raw].load
            print "*" * 42
        content = packet[Raw].load

        try:
            # Edit here. Modify content.
            content = content.replace("HTTP/1.1","HTTP/1.0")

            packet[Raw].load = content
        except UnicodeDecodeError:
            pass

        if debug:
            print "*" * 10 + " Package load modifed " + "*" * 10
            print packet[Raw].load
            print "*" * 42
    # recalculate length and checksum
    packet[IP].len = len(str(packet))
    packet[TCP].len = len(str(packet[TCP]))
    del packet[IP].chksum,packet[TCP].chksum
    # send packet modifed
    payload.set_verdict_modified(nfqueue.NF_ACCEPT, str(packet), len(packet))#set the packet content to our modified version

