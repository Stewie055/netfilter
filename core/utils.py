import os
import logging
import re
import sys

from core.logger import logger
from scapy.all import get_if_addr, get_if_hwaddr, get_working_if

formatter = logging.Formatter("%(asctime)s [Utils] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
log = logger().setup_logger("Utils", formatter)


def set_ip_forwarding(value):
    log.debug("Setting ip forwarding to {}".format(value))
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as file:
        file.write(str(value))
        file.close()

def get_iface():
    iface = get_working_if()
    log.debug("Interface {} seems to be up and running")
    return iface

def get_ip(interface):
    try:
        ip_address = get_if_addr(interface)
        if (ip_address == "0.0.0.0") or (ip_address is None):
            shutdown("Interface {} does not have an assigned IP address".format(interface))

        return ip_address
    except Exception as e:
        shutdown("Error retrieving IP address from {}: {}".format(interface, e))

def get_mac(interface):
    try:
        mac_address = get_if_hwaddr(interface)
        return mac_address
    except Exception as e:
        shutdown("Error retrieving MAC address from {}: {}".format(interface, e))

class Qmode:
    INPUT = 'i'
    OUTPUT = 'o'
    FORWARD = 'f'

class iptables:

    dns     = False
    http    = False
    smb     = False
    nfqueue = False

    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def flush(self):
        log.debug("Flushing iptables")
        os.system('iptables -F && iptables -X && iptables -t nat -F && iptables -t nat -X')
        self.dns  = False
        self.http = False
        self.smb  = False
        self.nfqueue = False

    def HTTP(self, http_redir_port):
        log.debug("Setting iptables HTTP redirection rule from port 80 to {}".format(http_redir_port))
        os.system('iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port {}'.format(http_redir_port))
        self.http = True

    def DNS(self, dns_redir_port):
        log.debug("Setting iptables DNS redirection rule from port 53 to {}".format(dns_redir_port))
        os.system('iptables -t nat -A PREROUTING -p udp --destination-port 53 -j REDIRECT --to-port {}'.format(dns_redir_port))
        self.dns = True

    def SMB(self, smb_redir_port):
        log.debug("Setting iptables SMB redirection rule from port 445 to {}".format(smb_redir_port))
        os.system('iptables -t nat -A PREROUTING -p tcp --destination-port 445 -j REDIRECT --to-port {}'.format(smb_redir_port))
        self.smb = True

    def NFQUEUE(self, mode=Qmode.FORWARD, cmd=None):
        log.debug("Setting iptables NFQUEUE rule")
        #os.system('iptables -I FORWARD -j NFQUEUE --queue-num 0')
        if cmd != None:
            log.debug("Using user's iptalbe." + cmd)
            os.system(cmd)
        elif mode == Qmode.INPUT:
            log.debug("Using input mode.")
            os.system('iptables -A INPUT  -j NFQUEUE')
        elif mode == Qmode.OUTPUT:
            log.debug("Using output mode.")
            os.system('iptables -A OUTPUT -j NFQUEUE')
        elif mode == Qmode.FORWARD:
            log.debug("Using forward mode.")
            os.system('iptables -I FORWARD -j NFQUEUE')
        else:
            log.debug("Error occurs setting iptables")
            sys.exit("Error occurs setting iptables")
        self.nfqueue = True
