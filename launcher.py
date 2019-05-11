from tkinter import *
import ipaddress, sys

lang = "Français"

def checkIP():
    try:
        ip = str(ipaddress.ip_address(entr1.get()))
        res1.configure(text = "IP OK : " + ip, fg = 'green')
        return ip
    except ValueError:
        res1.configure(text="Adresse IP invalide", fg = 'red')
        return False

def checkPort():
    try:
        port = int(entr2.get())
        if 0 <= port <=65535:
            res2.configure(text = "Port OK : " + str(port), fg = 'green')
            return port
        else:
            raise ValueError
    except ValueError:
        res2.configure(text = "Port invalide", fg = 'red')
        return False

def updateLocale(event):
    global lang

    try:
        lang = listbox.get(listbox.curselection())
    except:
        pass

def launchGame():
        ip = checkIP()
        port = checkPort()

        if lang == "Français": locale = "fr"
        else: locale = "en"

        if ip and port:
            fen1.destroy()
            print("[Launcher] Lancement du jeu...\n")
            sys.argv = ["start.py", ip, port, locale]
            import start
        else:
            print("[Launcher] Les informations saisies sont invalides.")

fen1 = Tk()
fen1.title('Coop Dungeon Adventure')
txt1 = Label(fen1, text = 'Adresse IP :', fg='black')
txt2 = Label(fen1, text = 'Port :', fg='black')
res1 = Label(fen1)
res2 = Label(fen1)
entr1 = Entry(fen1)
entr2 = Entry(fen1)
bouQ = Button(fen1, text='Quitter', fg='red', command=fen1.destroy)
bouL = Button(fen1, text='Lancer', fg='blue', command=launchGame, width=16, height=2, font=('Arial', 16))
can1 = Canvas(fen1, width=124, height=124, bg='white')
photo = PhotoImage(file ='game/resources/launcher.png')
item = can1.create_image(62, 62, image=photo)

listbox = Listbox(fen1, width=8, height=2)
listbox.insert(0, 'Français')
listbox.insert(1, 'English')
listbox.select_set(0)
listbox.bind("<<ListboxSelect>>", updateLocale)

txt1.grid(row=0)
res1.grid(row=1, column=1)
txt2.grid(row=2)
res2.grid(row=3, column=1)
can1.grid(row=0, column=3, rowspan=4, columnspan=2, padx=6, pady=3)
entr1.grid(row =0, column =1, columnspan=2)
entr2.grid(row =2, column =1, columnspan=2)
bouL.grid(row=4, column=1, columnspan=3)
bouQ.grid(row=4, column=0)
listbox.grid(row=4, column=4, sticky='e')

fen1.mainloop()