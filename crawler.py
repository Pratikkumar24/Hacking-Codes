import requests


def request(url):
    try:
        return requests.get("http://"+url)
    except requests.exceptions.ConnectionError:
        pass

url = "10.0.2.6/mutillidae/"
with open("/root/PycharmProjects/commonDir","r") as wordfile:
    for line in wordfile:  #for looping each line in the word, but it contains a "\n" at the end
        word = line.strip() #.strip() was to remover white space char
        test = url +"/"+word
        responses = request(test)
        if responses:
            print("[+]Discovered Url--> "+ test)

