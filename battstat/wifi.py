#!/usr/bin/env python
"""
Code from http://hackoftheday.securitytube.net/2013/03/wi-fi-sniffer-in-10-lines-of-python.html
"""
from scapy.all import *
ap_set = set()

def PacketHandler(pkt):
	if pkt.haslayer(Dot11) and (pkt.type, pkt.subtype) == (0, 0) and pkt.addr2 not in ap_set:
		ap_set.add(pkt.addr2)
		print "AP MAC: {} with SSID {}".format(pkt.addr2, pkt,info)

sniff(iface="wlp2s0", prn=PacketHandler)
