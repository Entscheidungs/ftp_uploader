import pysftp
import credenziali
import os
import json
import time


path_registro = "/home/chris/Documents/Python/reg.json"
path_files = "/home/chris/Documents/desk/"


def ottieni_modifiche():
    with pysftp.Connection(host=credenziali.myHostname, username=credenziali.myUsername, password=credenziali.myPassword) as sftp:
        remoteFilePath = '/root/ftp/modifiche.json'
        localFilePath = path_registro
        sftp.get(remoteFilePath, localFilePath) #per il get devi prima mettere il percorso remoto e poi quello locale


def crea_path(path):
    percorso = path.split('/')[:-1]
    p = ""
    for _x in range(len(percorso)):
         p+=percorso[_x]+"/"
         os.system(f"mkdir {p}")

    


def upload_con_confronto():
    trasferiti,totali,errori = 0,0,0
    lista_errori = []
    f = open(path_registro)
    with pysftp.Connection(host=credenziali.myHostname, username=credenziali.myUsername, password=credenziali.myPassword) as sftp:
            l = json.load(f)
            for p_file in l:
                    nome_file = p_file[::-1][:p_file[::-1].find("/")][::-1]
                        #! caso speciale
                    if nome_file[0] == ".":
                        continue
                    totali+=1
                    path_locale = p_file.replace("/chris/",path_files)
                    if os.path.exists(path_locale):
                        modifica_locale = os.path.getmtime(path_locale)
                        modifica_remoto = l[p_file]
                        if modifica_locale < modifica_remoto:
                            print(f"entra {path_locale}")
                            sftp.get(p_file,path_locale)
                            trasferiti+=1
                    else:
                        try:
                            os.system(f"touch {path_locale}")
                            sftp.get(p_file,path_locale)
                            print("trasferito")
                            trasferiti+=1
                        except:
                            print(f"errore {path_locale} ")
                            crea_path(path_locale)
                            lista_errori.append((p_file,path_locale))
                    

            for elm in lista_errori:
                try:
                     sftp.get(elm[0],elm[1])
                except:
                     errori+=1
            print(f"Files analizzati: {totali}\nFiles trasferiti: {trasferiti}\nFiles non trasferiti: {errori}")


while True:

    ottieni_modifiche()
    upload_con_confronto()
    time.sleep(3)

