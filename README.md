# Ftp_uploader
Uploader ftp che controlla ogni x minuti se ho modificato dei file e nel caso li invia ad un vps che uso come storage, nel caso io perda i file o abbia bisogno di un backup. Il programma presenta molti problemi, è ancora alla sua versione base:

-E' hardcodato
-Ha dei problemi per cui quando creo una nuova cartella devo eseguire un upload ricorsivo di tutti i file, in quanto il programma ha problemi nel creare una nuova directory nel server remoto
-Presenta un sistema inefficiente sempre per quanto riguarda l'hardcoding: avendo pensato ad un uso personale per questo script ho usato praticamente lo stesso path sia sul pc sia sul server:
  
    for file in Path("/home/chris/Documenti/Studio").rglob("*.*"):
                path_remoto = "/root/"+str(file)[12:]
                
Aggiungendo solo */root/* all'inizio
Andando avanti migliorerò questo codice, che per ora è solo qualcosa creato da me per me, ma forse in futuro risulterà utile (ed utilizzabile) a qualcuno
