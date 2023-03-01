import paramiko
import time
import credenziali
import pysftp
import os
from pathlib import *
import json
from datetime import datetime

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None  
err = []
def trova_percorsi(path,diz):
    percorso = path.split('/')[:-1]
    for _x in range(len(percorso)):
        diz[str(path)].append("/".join(percorso[:_x+1])+"/")
        #print(f"in {str(path)} ho aggiunto, {diz[str(path)]}")
    return diz


def ottieni_modifiche():
    with pysftp.Connection(host=credenziali.myHostname, username=credenziali.myUsername, password=credenziali.myPassword, cnopts=cnopts) as sftp:
        remoteFilePath = '/root/ftp/modifiche.json'
        localFilePath = '/home/chris/Documents/Script/ftp/reg.json'
        sftp.get(remoteFilePath, localFilePath) #per il get devi prima mettere il percorso remoto e poi quello locale


def upload_con_confronto():
    trasferiti  = [] #lista file trasferiti
    lista_errori = []
    locale = "/home/chris/desk/"
    f = open("/home/chris/Documents/Script/ftp/reg.json")
    diz = json.load(f)
    time.sleep(2)
    with pysftp.Connection(host=credenziali.myHostname, username=credenziali.myUsername, password=credenziali.myPassword, cnopts=cnopts) as sftp:
            
            for file in Path(locale).rglob("*.*"):
                p_file = str(file)
                path_remoto = p_file.replace(locale,"/chris/")
                modifica_locale = os.path.getmtime(p_file)
                try:
                    modifica_remoto = diz[path_remoto]
                    if modifica_locale > modifica_remoto:
                        sftp.put(p_file,path_remoto)
                        trasferiti.append(p_file)

                except KeyError:
                        try:
                            sftp.put(p_file,path_remoto)
                            trasferiti.append(p_file)
                        except:
                            if path_remoto not in diz.keys():
                                diz[path_remoto] = []
                            diz = trova_percorsi(path_remoto,diz)
                            lista_errori.append(p_file)
                
                except IsADirectoryError:
                    pass
                except FileNotFoundError:
                    err.append(p_file)
                

            riscrivi_errori(lista_errori,diz)
def riscrivi_errori(lista_errori,diz):
    global err
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(credenziali.myHostname, username=credenziali.myUsername, password=credenziali.myPassword)
    locale = "/home/chris/desk/"
    with pysftp.Connection(host=credenziali.myHostname, username=credenziali.myUsername, password=credenziali.myPassword, cnopts=cnopts) as sftp:
        for p in lista_errori:
            path_remoto = p.replace(locale,"/chris/")
            try:
                sftp.put(p,path_remoto)
            except:
                for x in diz[path_remoto]:
                    comando = "mkdir "+x
                    client.exec_command(comando)
            try:
                sftp.put(p,path_remoto)
            except IsADirectoryError:
                pass
            except FileNotFoundError:
                pass
                #print(p)
                #err.append(p)
                
    client.close()


while True:
    ottieni_modifiche()
    upload_con_confronto()
    time.sleep(10)
