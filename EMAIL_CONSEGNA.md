# Email di consegna — Il Consigliere

Questa e' la fonte unica del testo con cui Il Consigliere arriva sul computer di
un cliente. Il prodotto e l'email evolvono insieme: ogni cambiamento che tocca
la repo, la cartella di installazione, il collaudo o l'esito richiesto aggiorna
anche questo file nello stesso commit.

La cronologia Git conserva i miglioramenti. I dati del singolo invio restano nel
testo mostrato a Sal, nella copia Gmail e nella scheda del cliente.

## Regola fissa: l'email e' una missione per l'agente del cliente

Il lettore operativo del corpo e' l'agente AI collegato alla casella del
cliente, secondo il modo `AGENTE_CON_POSTA` della procedura
`commerciale/procedure/email_operativa_versionata.md`. L'agente legge la
missione in Gmail e parte dalla prima azione: scarica il kit dalla repo
pubblica, lo installa, ripara da solo cio' che serve, collauda e chiude con un
resoconto reale.

Al proprietario restano soltanto le conferme di sicurezza del sistema, gli
accessi e le scelte che appartengono a lui. Il blocco `SITUAZIONE IN BREVE`
apre il messaggio e lo rende leggibile anche da lui e da Sal.

Quando la posta dell'agente e' ancora da collegare, si usa il modo
`PERSONA_CON_PASSAGGIO` e il proprietario riceve un unico blocco autosufficiente
da consegnare al suo agente.

## Dati da compilare e verificare

Prima di mostrare l'email a Sal, sostituisci tutti i campi tra parentesi quadre
usando fonti verificate:

- `[NOME]`: nome del destinatario, dalla sua scheda cliente;
- `[EMAIL_DESTINATARIO]`: indirizzo verificato del destinatario;
- `[AZIENDA]`: ragione sociale usata nell'oggetto del resoconto;
- `[CARTELLA_KIT]`: cartella locale di installazione, in forma portabile;
- `[CARTELLA_KIT_POWERSHELL]`: lo stesso percorso nella forma della shell usata;
- `[COMMIT]`: commit pubblicato su `main` al momento dell'invio;
- `[VERSIONE]`: contenuto di `VERSION` a quel commit;
- `[FIRMA_AGENTE]`: agente LeaderAI che ha preparato e verificato la consegna.

Repo pubblica: `salChiarenza/il-consigliere`,
`https://github.com/salChiarenza/il-consigliere`.

## Cartella di installazione: locale, fuori dalle cartelle sincronizzate

Il kit e' un repository Git. Un repository dentro OneDrive, SharePoint, Drive o
qualsiasi altra cartella sincronizzata viene riscritto dal servizio di
sincronizzazione mentre Git sta lavorando sugli stessi file, e la copia si
corrompe. Per Villa la regola e' stata concordata nella sessione del
09/07/2026 ed e' valida per ogni cliente.

Percorsi standard, in forma portabile:

- Windows: `%USERPROFILE%\il-consigliere` (`$env:USERPROFILE\il-consigliere` in
  PowerShell);
- Mac: `~/il-consigliere`.

Il report della settimana e il catalogo dei consigli sono documenti normali:
nascono nella casa condivisa in cui l'agente lavora gia' con il cliente, cosi'
restano visibili a tutto il gruppo. Un percorso assoluto entra nell'email
soltanto dopo essere stato letto su quel computer, in un rapporto del cliente o
nella sua scheda.

## Formato di invio

Il blocco email e' scritto in Markdown ed e' la fonte unica per entrambe le
parti del messaggio:

- il corpo HTML e il fallback `text/plain` nascono dallo stesso testo;
- il connettore Gmail riceve il blocco Markdown;
- `tools/gmail/gmail_send.py` riceve insieme `--body-file` e `--html-file`;
- nell'HTML la destinazione compare come testo cliccabile e l'indirizzo esteso
  vive nella parte testuale;
- il comando `git clone` resta testo semplice e identico nelle due parti,
  perche' l'agente lo esegue alla lettera.

## Oggetto

**Prima consegna:** `Il Consigliere: installazione e primo report dei consumi AI`

**Versione corretta:** `Il Consigliere: istruzioni aggiornate`

## Testo

```text
SITUAZIONE IN BREVE
Cosa funziona: Il Consigliere e' pronto e pubblicato nella repo LeaderAI, versione [VERSIONE], commit [COMMIT]. Legge in locale come vengono usati Claude Code e Codex e mostra dove finiscono davvero i consumi.
Cosa completiamo: il tuo agente scarica il kit, lo installa in una cartella locale del computer, lo collauda e produce il primo report della settimana.
Cosa serve da te: le conferme di sicurezza di Windows, nel momento preciso in cui il tuo agente te le presenta.
Quando si chiude: quando il primo report e' leggibile nella casa condivisa e a noi arriva il resoconto finale.

Questa missione operativa e' per l'agente AI che gestisce l'ambiente di [NOME].

RISULTATO ATTESO
Il Consigliere installato e funzionante su questo computer, il primo report della settimana leggibile da [NOME], un solo resoconto finale inviato a sal@salchiarenza.com.

FONTE
Repo pubblica LeaderAI [il-consigliere su GitHub](https://github.com/salChiarenza/il-consigliere), aperta in lettura da qualunque computer. Versione di questa consegna: commit [COMMIT].

DOVE VA IL KIT
Installa in [CARTELLA_KIT], sul disco locale del computer. In PowerShell lo stesso percorso si scrive [CARTELLA_KIT_POWERSHELL]. Il kit e' un repository Git: tenendolo fuori da OneDrive e da SharePoint, Git resta l'unico a scrivere su quei file, anche mentre la cartella condivisa si aggiorna. La regola vale per [NOME] dalla sessione del 09/07/2026.
Il report della settimana e il catalogo dei consigli sono documenti normali: creali nella casa condivisa in cui lavori gia' con [NOME], cosi' li vede tutto il gruppo.

SEQUENZA
1. Controlla che Git sia presente su questo computer e installalo se serve, cosi' il passo successivo parte al primo colpo. Poi posizionati nella cartella utente ed esegui:
git clone https://github.com/salChiarenza/il-consigliere.git
Cosi' nasce [CARTELLA_KIT]. Controlla che il commit sia [COMMIT] o successivo.
2. Leggi integralmente INSTALLA_CON_AI.md nella cartella appena creata ed esegui la missione di installazione che contiene, passo per passo.
3. Rileva tu quale motore gira su questo computer, Claude Code oppure Codex, e installa la parte corrispondente. Il kit legge entrambi i motori e resta completo anche con uno solo presente: la sezione dell'altro motore dichiara che quel motore e' assente.
4. Verifica il resto dell'ambiente e sistemalo da solo: Python e i componenti richiesti. Su Windows il comando Python e' `py` quando `python3` risulta assente. Installa cio' che serve e riprendi da dove ti eri fermato.
5. Esegui il collaudo del kit: la raccolta dati locale, poi le due modalita' SETTIMANA e ADESSO.
6. Genera il primo report della settimana e mostralo a [NOME] in parole semplici, con i numeri veri delle sue conversazioni.

QUANDO QUALCOSA SI FERMA
Leggi il messaggio, individua la causa, correggila e ripeti il passo. Continua fino al collaudo completo. I dati restano tutti su questo computer.

GESTI CHE RESTANO A [NOME]
Presentagli una richiesta alla volta, nel momento preciso in cui serve: una conferma di sicurezza di Windows, un accesso, una scelta che appartiene a lui. Il lavoro tecnico resta tuo.

CRITERIO DI RIUSCITA
La raccolta dati gira fino in fondo, le due modalita' rispondono, il report della settimana esiste ed e' scritto in modo che una persona lo capisca al primo colpo.

CHIUSURA
Salva stato e prove nella casa condivisa. Poi manda una sola email a sal@salchiarenza.com, oggetto `Il Consigliere: esito installazione [AZIENDA]`, con dentro:
- cosa hai installato e in quale cartella;
- cosa hai provato davvero;
- cosa funziona, con la prova concreta;
- cosa resta aperto e per quale motivo.
Questa e' l'unica email del ciclo: lavora fino alla fine e chiudi con l'esito reale. Poi archivia questo messaggio.

A presto,

Sal & [FIRMA_AGENTE]
```

## Controllo prima dell'invio

1. Apri `commerciale/INDEX.md`, la scheda del cliente e il suo `STATUS.md`;
   identifica l'agente che tiene il filo e la casa in cui lavora.
2. Cerca `in:sent newer_than:1d to:[EMAIL_DESTINATARIO]` e confronta oggetto,
   scopo e versione. Registra `SENT_DUPLICATE_CHECK_OK` e
   `CLIENTE_COORDINATO_OK`.
3. Verifica che la repo sia pubblica e che il commit indicato esista su `main`.
4. Compila ogni campo tra parentesi quadre da fonti verificate e rileggi ogni
   percorso: forma portabile, oppure valore letto su quella macchina.
5. Ripeti il percorso del destinatario con il suo stesso livello di accesso:
   clona la repo senza credenziali, entra nella cartella, completa
   installazione e primo collaudo sul sistema operativo previsto. Registra
   `PROVA_DESTINATARIO_OK` soltanto dopo questa prova reale.
6. Dichiara il lettore operativo: `LETTORE_AGENTE_OK` quando l'agente del
   cliente legge Gmail, `LETTORE_PERSONA_OK` con `CONSEGNA_OK` per la prima
   configurazione.
7. Rileggi il testo nella prospettiva dell'agente: ogni verbo parla a lui,
   `SITUAZIONE IN BREVE` precede le istruzioni, i gesti umani sono richieste
   che l'agente presenta al proprietario.
8. Controlla `tu`, frasi affermative, firma a due nomi, zero em dash, link
   cliccabile nell'HTML e indirizzo esteso nella parte testuale.
9. Mostra a Sal destinatario, oggetto e testo integrale. Dopo il suo comando
   esplicito registra `INVIO_OK` e manda una sola nuova email con oggetto
   autonomo.
10. Rileggi la copia in Sent, conferma che ne esista una sola, applica la label
    del cliente, aggiorna la sua scheda e lascia la Inbox ordinata.

**Stato del gate al 21/08/2026:** il percorso completo del destinatario su
Windows resta da eseguire, quindi `PROVA_DESTINATARIO_OK` e' ancora da
guadagnare. Il primo invio parte dopo quel collaudo.

## Miglioramento continuo

Quando una consegna incontra un ostacolo:

1. raccogli la prova reale, come messaggio, screenshot o codice di uscita;
2. identifica il punto proprietario: email, repo, installer, procedura o
   ambiente del cliente;
3. correggi il punto proprietario e aggiorna questo file quando cambia
   l'esperienza del destinatario;
4. aggiorna `VERSION` e `CHANGELOG.md`;
5. ripeti il percorso completo del destinatario;
6. pubblica su `main` e riparti dalla repo pubblica nell'invio successivo.

Caso di origine: 20/07/2026, Fabrizio Villa. La repo era privata, il suo agente
ha ricevuto GitHub 404 e ha prodotto un'analisi locale alternativa al posto del
report del kit. Da li' nascono la repo pubblica, il commit dichiarato
nell'email e la prova del percorso del destinatario.
