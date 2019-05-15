from tkinter import * # On importe la librairie graphique Tkinter
import ipaddress, sys # et également une librairie pour le traitement des addresses IP

languages = [["French", "fr"], ["English", "en"]] # On indique les différentes langues disponibles et leur code associé

def checkIP(): # On définit une fonction pour vérifier l'adresse IP entrée par l'utilisateur
	try: # On teste la validité de l'adresse IP
		ip = str(ipaddress.ip_address(ipInput.get())) # Transformation de l'adresse IP en une suite de caractères
		return ip # On retourne sa valeur si elle est valide
	except ValueError:
		ipMessageLabel.configure(text="Adresse IP invalide", fg = 'red') # Si ce n'est pas le cas, on affiche à l'utilisateur un message d'erreur en rouge
		print("[Launcher] L'IP saisie est invalide.")
		return False

def checkPort(): # On définit une fonction pour vérifier le du port entré par l'utilisateur
	try:
		port = int(portInput.get())
		if 0 <= port <=65535: # Un port est compris entre 0 et 65535, on vérifie donc que la valeur entrée par l'utilisateur est comprise dans cette encadrement
			return port
		else:
			raise ValueError
	except ValueError:
		portMessageLabel.configure(text = "Port invalide", fg = 'red') # Si ce n'est pas le cas, on affiche à l'utilisateur un message d'erreur en rouge
		print("[Launcher] Le port saisie est invalide (doit être compris entre 0 et 65535)")
		return False

def checkLangIndex(): # On définit une fonction qui permet de récupérer la langue à partir de la sélection de l'utilisateur
	try:
		langIndex = langSelector.curselection()[0] # Si il s'agit d'une sélection, on stocke le nom de la langue sélectionnée
		return langIndex
	except:
		print("[Launcher] Auncune langue n'a été sélectionnée.")
		return -1 # Si rien n'est sélectionné, on renvoi -1 pour indiquer une erreur

def launchGame():
		ip = checkIP() # On récupère les différentes valeurs saisies. La variable sera à False en cas de saisie invalide
		port = checkPort()
		langIndex = checkLangIndex()

		if langIndex >= 0:
			lang = languages[langIndex][1] # On récupère le code de langue à partir de son nom (Français -> fr, English -> en...)
		else:
			lang = False

		if ip and port and lang:
			window.destroy() # On ferme la fenêtre car nous n'en avons plus besoin
			print("[Launcher] Lancement du jeu...\n")
			sys.argv = ["start.py", ip, port, lang]
			import start  # On importe le script de lancement du jeu

window = Tk() # On crée une fenêtre grâce à la bibliothèque Tkinter
window.title('Coop Dungeon Adventure') # On définit le titre de cette fenêtre

ipLabel = Label(window, text = 'Adresse IP :') # On crée une étiquette pour le champ de saisie de l'IP
ipInput = Entry(window) # On ajoute le champ de saisie associé
ipMessageLabel = Label(window) # On laisse un espace pour afficher un message en cas d'erreur

portLabel = Label(window, text = 'Port :') # On crée une étiquette pour le champ de saisie du port
portInput = Entry(window) # On ajoute le champ de saisie associé
portMessageLabel = Label(window) # On laisse un espace pour afficher un message en cas d'erreur

quitButton = Button(window, text='Quitter', fg='red', command=window.destroy) # On crée le bouton permettant de quitter le launcher en l'associant à sa fonction
launchButton = Button(window, text='Lancer', fg='blue', command=launchGame, width=16, height=2, font=('Arial', 16)) # De même, on crée le bouton permettant lancer le jeu

image = PhotoImage(file ='game/resources/launcher.png') # On importe l'image à afficher
canvas = Canvas(window, width=124, height=124) # On crée un canvas qui nous permettra de l'afficher
canvas.create_image(62, 62, image=image) # Enfin, on ajoute l'image au cadre pour l'afficher

langSelector = Listbox(window, width=8, height=len(languages)) # On définit une liste séléctionnable du même nombre de lignes que de langages
for i in range(0, len(languages)): # On fait le tour des langages disponibles pour les ajouter un par un à la liste
	langSelector.insert(i, languages[i][0])

ipLabel.grid(row=0) # On met en page la fenêtre grâce à un système de lignes et colonnes
ipMessageLabel.grid(row=1, column=1)
portLabel.grid(row=2)
portMessageLabel.grid(row=3, column=1)
canvas.grid(row=0, column=3, rowspan=4, columnspan=2, padx=6, pady=3)
ipInput.grid(row =0, column =1, columnspan=2)
portInput.grid(row =2, column =1, columnspan=2)
launchButton.grid(row=4, column=1, columnspan=3)
quitButton.grid(row=4, column=0)
langSelector.grid(row=4, column=4, sticky='e')

window.mainloop() # On lance la boucle principale qui permettra d'afficher la fenêtre
