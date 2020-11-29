import requests
import re,html
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Scanner:
    def __init__(self,url,ignore_links):
        self.session = requests.Session()
        self.target_url = url
        self.target_list=[]
        self.links_to_ignore = ignore_links

    def extract_link_from(self,url):
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?)"', (response.content).decode(errors="ignore"))

    def crawl(self,url=None):
        if url==None:
            url = self.target_url
        links = self.extract_link_from(url)
        for link in links:
            link = urljoin(url, link)

            if "#" in link:
                link = link.split('#')[0]

            if (self.target_url) in (link) and (link) not in (self.target_list) and (link) not in (self.links_to_ignore) :
                self.target_list.append(link)
                print(link)
                self.crawl(link)

    def extract_forms(self,url):
        html_code = self.session.get(url).content
        parsed_code = BeautifulSoup(html_code, "html.parser")
        return parsed_code.findAll("form")

    def submit_forms(self, form, value, url):
        action_name = form.get("action")
        actions = urljoin(url, action_name)
        method_name = form.get("method")
        input_names = form.findAll("input")
        post_data = {}

        for input in input_names:
            in_name = input.get("name")
            in_type = input.get("type")
            in_value = input.get("value")
            if in_type == "text":
                in_value = value
            post_data[in_name] = in_value
        if method_name == "post":
            return self.session.post(actions, data=post_data)
        else:
            return self.session.get(actions, params = post_data)

    def run_scanner(self):
        for links in self.target_list:
            forms = self.extract_forms(links)
            for form in forms:
                print("[+] Testing for the form in " + str(links))
                is_vulnreable_to_xss = self.test_xss_forms(form, links)
                if is_vulnreable_to_xss:
                    print("***] Discovered xss in "+  str(links) +" of FORM->")
                    print(form)
                    print("\n\n")
            if "=" in links:
                print("[+] Testing for the link: "+  str(links))
                is_vulnreable_to_xss = self.test_xss_links( links)
                if is_vulnreable_to_xss:
                    print("[***] Discovered xss in " +  str(links))
                    print("\n\n")


    def test_xss_forms(self, form, url):
        xss_test_script = "<sCript>alert('Hello')</scriPt>"
        response = self.submit_forms(form, xss_test_script, url)
        return xss_test_script in html.unescape(response.content.decode())

    def test_xss_links(self, url):
        xss_test_script = "<sCript>alert('Hello')</scriPt>"
        url = url.replace("=","="+xss_test_script)
        response = self.session.get(url)
        return xss_test_script in html.unescape(response.content.decode())

