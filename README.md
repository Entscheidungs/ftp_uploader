Questo programma controlla periodicamente se sono state effettuate modifiche all'interno di una determinata directory, come ad esempio la modifica/creazione di un file o di una subdirectory ed utilizza il protocollo SFTP (tramite la libreria pysftp) ed invia i file modificati ad un server remoto che funge da archiviazione, il che può essere utile per varie evenienze:

- Perdita dei dati sulla propria macchina
- Necessità di accedere a quei dati da un'altra macchina o comunque da remoto
- Necessità di tornare ad una versione precedente di un file modificato 

Ad esempio, mi è capitato di modificare un programma e di avere bisogno di una versione precedente di esso, e con undo non riuscivo a tornare a quella versione precedente, ma il programma era stato caricato precedentemente sulla macchina remota, e quindi ho potuto accedere alla versione precedente.
Il percorso è hardcoded (bisogna modificare il programma nel caso si voglia cambiare percorso di partenza e di destinazione).
Le credenziali vengono trasmesse in chiaro come argomenti delle funzioni.


Il file _monitora_modifiche.py_ è presente sulla macchina remota, che periodicamente controlla tutte le date di ultima modifica dei file, che poi verranno lette dal programma locale e confrontate con quelle dei file locali.
