import pysftp
import paramiko
import time
import credenziali
import os
from pathlib import *
import json

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

path_registro = "/home/chris/Documents/Script/ftp/reg.json"
path_files = "/home/chris/desk/"


err = []
def trova_percorsi(path,diz):
    percorso = path.split('/')[:-1]
    for _x in range(len(percorso)):
        diz[str(path)].append("/".join(percorso[:_x+1])+"/")
        print(f"in {str(path)} ho aggiunto, {diz[str(path)]}")
    return diz


def ottieni_modifiche():
    with pysftp.Connection(host=credenziali.myHostname, username=credenziali.myUsername, password=credenziali.myPassword, cnopts=cnopts) as sftp:
        remoteFilePath = '/root/ftp/modifiche.json'
        localFilePath = path_registro
        sftp.get(remoteFilePath, localFilePath) #per il get devi prima mettere il percorso remoto e poi quello locale



def crea_path(path):
    print(f"entra {path}")
    percorso = path.split('/')[:-1]
    p = ""
    for _x in range(len(percorso)):
         p+=percorso[_x]+"/"
         print(p)
         os.system(f"mkdir {p}")

    


def upload_con_confronto():
    global err
    #c = 0 #contatore
    trasferiti  = [] #lista file trasferiti
    lista_errori = []
    f = open(path_registro)
    with pysftp.Connection(host=credenziali.myHostname, username=credenziali.myUsername, password=credenziali.myPassword, cnopts=cnopts) as sftp:
            l = json.load(f)
            for p_file in l:
                    nome_file = p_file[::-1][:p_file[::-1].find("/")][::-1]
                        #! caso speciale
                    if nome_file[0] == ".":
                        continue
                    #print("entra")
                    path_locale = p_file.replace("/home/Documenti/Studio/",path_files)
                    if os.path.exists(path_locale):
                        modifica_locale = os.path.getmtime(path_locale)

                        #print(path_locale)
                        modifica_remoto = l[p_file]
                        #print(p_file)
                        #print(path_locale)
                        if modifica_locale < modifica_remoto:
                            sftp.get(p_file,path_locale)
                            trasferiti.append(p_file)
                    else:
                        try:
                            os.system('echo %s|sudo -S %s' % (credenziali.myPcPassword, f"touch {path_locale}"))
                            sftp.get(p_file,path_locale)
                            trasferiti.append(path_locale)
                        except:
                            print(f"errore {path_locale} ")
                            crea_path(path_locale)
                            lista_errori.append((p_file,path_locale))
                    
            #riscrivi_errori(lista_errori,diz)

            print
            for elm in lista_errori:
                sftp.get(elm[0],elm[1])
def riscrivi_errori(lista_errori,diz):
    global err
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(credenziali.myHostname, username=credenziali.myUsername, password=credenziali.myPassword)

    with pysftp.Connection(host=credenziali.myHostname, username=credenziali.myUsername, password=credenziali.myPassword, cnopts=cnopts) as sftp:
        for p in lista_errori:
            print(p)
            path_remoto = p.replace(path_files,"/home/Documenti/Studio/")
            try:
                sftp.get(p,path_remoto)
            except:
                for x in diz[path_remoto]:
                    comando = "mkdir "+x
                    client.exec_command(comando)

            try:
                sftp.get(p,path_remoto)
            except IsADirectoryError:
                pass
            except FileNotFoundError:
                err.append(p)
                
    client.close()

def upload_totale():
    with pysftp.Connection(host=credenziali.myHostname, username=credenziali.myUsername, password=credenziali.myPassword, cnopts=cnopts) as sftp:
        print("entra")
        sftp.get_r("/home/Documenti/Studio/Programmazione/go",path_files)
        #! get_r copia male i files
    #ottieni_modifiche()
ottieni_modifiche()
upload_con_confronto()
os.system(f"sudo chmod 777 -R {path_files}")


#upload_totale()