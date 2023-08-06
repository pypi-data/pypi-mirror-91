import requests
from getpass import getpass
from termcolor import cprint

def login():
    
    print("\t\t\t\t\t"+"-"*33)
    print("\t\t\t\t\t"+"|\t"+"                 \t|")
    print("\t\t\t\t\t"+"|\t"+"Login en HostHome\t|")
    print("\t\t\t\t\t"+"|\t"+"                 \t|")
    print("\t\t\t\t\t"+"-"*33)

    mail = input("Porfavor escribe tu email :: ")
    psw = getpass("Escribe tu contraseña :: ")
    
    data = requests.get(f"http://127.0.0.1:5000/api/admin/getuser?mail={mail}&psw={psw}").json()

    if data == {}:
        cprint("Esa cuenta no existe intentalo otra vez", "red")
        exit(0)

    return data
