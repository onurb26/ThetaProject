import socket, http.client,ipaddress, colorama
from colorama import Fore

def validateIp(): # Controlla se l'ip è inserito correttamente
   while True:
      ip = input("Inserisci l'ip da scansionare o digita '0' per uscire :\n")
      if ip=="0":
         break
      try:
        ipaddress.ip_address(ip)
        break
      except ValueError:
        print("IP non valido, Riprova!")
   return ip

def portScan():
	ip=validateIp()
	if ip=="0":
		return
	try:
		port_range = input("Inserire il range di porte da scannerizzare (es 60-65):\n")
		port_range = list(map(int,port_range.split("-")))
		port_range.sort()   #Ordinamento in ordine crescente
		flag=0 
		for port in range(port_range[0], port_range[1]):
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.settimeout(1)
				result = sock.connect_ex((ip, port))
				if result == 0:
					print(f"Porta {Fore.GREEN}{port} --> {socket.getservbyport(port)}{Fore.WHITE}")
					flag=1
				sock.close()
			except:
				continue
		if flag==0:
			print(f"{Fore.RED}Nessuna porta aperta{Fore.WHITE}\n")
	except:
		print ("C'è un errore, riprova.\n")

def metodiHTTP():
	host=validateIp()
	if host == '0':
	  return
	while True: # Controllo input porta
		port = ""
		port = input("Inserire la porta target (0-65535, default: 80): ")
		if port == "":
			port = 80
			break
		elif port.isdigit() and int(port) >= 0 and int(port) <= 65535:
			break
		else:
			print ("C'è un errore, riprova.\n")
	path = input("Inserisci un PATH: ")

	try:
		connection = http.client.HTTPConnection(host, port) # crea un oggetto per gestire la connessione
		connection.request("OPTIONS",path)
		response = connection.getresponse() # invia una richiesta in base hai parametri scelti
		allowed_methods = response.getheader("Allow")
		if allowed_methods != None:
			print("Metodi abilitati: ", Fore.GREEN, allowed_methods, Fore.WHITE) # stampa la risposta del server
		else:
			print(f"{Fore.RED}OPTIONS {Fore.WHITE}non ha restituito nessun risultato, inserire manualmente il metodo HTTP da testare.")
			allowed_methods = input("Inserire i metodi da testare separati da virgola (es. GET,POST,PUT): ")
			methods = allowed_methods.upper().split(",")
			for method in methods:
					connection = http.client.HTTPConnection(host, port) # crea un oggetto per gestire la connessione
					connection.request(method, path)
					response = connection.getresponse() # invia una richiesta in base ai parametri scelti
					if response.status >= 200 and response.status <= 213 :
						print(f"Metodo {Fore.GREEN}{method}{ Fore.WHITE} funzionante.")
						connection.close()
					else:
						print(f"Metodo {Fore.RED}{method}{Fore.WHITE} non funzionante.\n")
						connection.close()

	except ConnectionRefusedError:
		print("Impossibile connettersi\n")

def menu():

	while True:
		scelta_programma = input("Scegli il programma da eseguire: [ 1 ] per port scan o [ 2 ] per enumerazione metodi HTTP abilitati o [ 0 ] per uscire: ")
		try:
			match  scelta_programma :
				case "0":
					break
				case "1":
        				portScan()
				case "2":
        				metodiHTTP()
				case _:
                			print ("Carattere non consentito\n")
		except:
			break


menu()
