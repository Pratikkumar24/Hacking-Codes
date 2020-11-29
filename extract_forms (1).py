import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin #use to parse the sub-links with the full link

target_url = "http://10.0.2.6/mutillidae/index.php?page=dns-lookup.php"


def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

html_code = request(target_url).content

parsed_code = BeautifulSoup(html_code, "html.parser")

formList = parsed_code.findAll("form")
for form in formList:
    action_name = form.get("action")
    actionUrl = urljoin(target_url,action_name)
    method_name = form.get("method")
    input_names = form.findAll("input")
    post_data={}

    for input in input_names:
        in_name= input.get("name")
        in_type = input.get("type")
        in_value = input.get("value")
        if in_type == "text":
            in_value = "text"
        post_data[in_name]=in_value
    response = requests.post(actionUrl, data = post_data)
    parse_response = BeautifulSoup(response.content, "html.parser")
    print(parse_response)
