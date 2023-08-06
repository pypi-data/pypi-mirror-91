import requests
from getpass import getpass
from termcolor import cprint

import webbrowser

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
        si_no = input("\n¿Quieres crearte una? [s/n] :: ")
        if si_no == "s":
            webbrowser.open('http://127.0.0.1:5000/login', new=2)
            return login()
        else:
            cprint("Veo que no", "red")
            exit(0)

    return data
