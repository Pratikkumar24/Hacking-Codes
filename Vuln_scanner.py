import scanner


target_url = "http://10.0.2.6/dvwa/"
data_dict = {"username":"admin","password":"password","Login":"submit"}
links_to_ignore = ["http://10.0.2.6/dvwa/logout.php"]
vuln_scanner = scanner.Scanner(target_url,links_to_ignore)
vuln_scanner.session.post("http://10.0.2.6/dvwa/login.php", data = data_dict)
vuln_scanner.crawl()
vuln_scanner.run_scanner()





# post = vuln_scanner.extract_forms("http://10.0.2.6/dvwa/vulnerabilities/xss_r/")
# print(post)
# response = vuln_scanner.test_xss_forms(post[0], "http://10.0.2.6/dvwa/vulnerabilities/xss_r/")
# print(response)