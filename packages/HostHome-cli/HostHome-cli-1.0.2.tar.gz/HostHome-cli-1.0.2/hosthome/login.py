import requests
from getpass import getpass

def login():
    
    print("-"*10)
    print("|\t"+"                 \t|")
    print("|\t"+"Login en HostHome\t|")
    print("|\t"+"                 \t|")
    print("-"*10)
    
    data = requests.get("http://127.0.0.1:5000/api/admin/getuser?mail={mail}&psw={psw}")
