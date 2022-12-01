import credenziali
import pysftp
import os
from pathlib import *
import modifiche
import importlib
import time


cnopts = pysftp.CnOpts()
cnopts.hostkeys = None  

def ottieni_modifiche():
    with pysftp.Connection(host=credenziali.myHostname, username="root", password=credenziali.myPassword, cnopts=cnopts) as sftp:
        localFilePath = '/home/chris/Documenti/script/ftp/modifiche.py'
        remoteFilePath = '/root/ftp/modifiche.py'
        sftp.get(remoteFilePath, localFilePath) #per il get devi prima mettere il percorso remoto e poi quello locale

def upload_totale():
    #questa funzione carica tutti i file e server per vedere quanto ci mette
    with pysftp.Connection(host=credenziali.myHostname, username="root", password=credenziali.myPassword, cnopts=cnopts) as sftp:
        sftp.put_r("/home/chris/Documenti/Studio","/root/Documenti/Studio")

def upload_con_confronto():
    c = 0 #contatore
    trasferiti  = [] #lista file trasferiti
    lista_errori = []
    with pysftp.Connection(host=credenziali.myHostname, username=credenziali.myUsername, password=credenziali.myPassword, cnopts=cnopts) as sftp:
            for file in Path("/home/chris/Documenti/Studio").rglob("*.*"):
                path_remoto = "/root/"+str(file)[12:]
                path_locale = str(file)
                print(path_remoto)
                try:
                    if modifiche.d[path_remoto] < os.path.getmtime(path_locale):
                        sftp.put(path_locale,path_remoto)
                        c+=1
                        trasferiti.append(path_locale)
                except KeyError:
                    try:
                        #se il percorso del file non viene trovato nel dizionario vuol dire che il file non c'è e quindi lo carico in quanto è nuovo
                        c+=1
                        trasferiti.append(path_locale)
                        sftp.put(path_locale,path_remoto)
                    except IsADirectoryError:
                        #se il programma incontra una cartella nascosta la invia a priori
                                c+=1
                                trasferiti.append(path_locale)
                                sftp.put_r(path_locale,path_remoto)
                                print("entra")
                    except FileNotFoundError:
                            #nel caso una cartella locale non esiste in remoto perché l'ho appena creata, purtroppo ora non riesco a rimediare a questa inefficienza, quindi carico tutta la cartella Studio interamente
                                upload_totale()
                                break
                except IsADirectoryError:
                    #se il programma incontra una cartella nascosta la invia a priori
                    #l'eccezione è gestita due volte in quanto a volte viene dopo il KeyError e a volte no
                            c+=1
                            trasferiti.append(path_locale)
                            sftp.put_r(path_locale,path_remoto)
while True:
    ottieni_modifiche()
    importlib.reload(modifiche)
    upload_con_confronto()
    time.sleep(300)

#upload_totale()
