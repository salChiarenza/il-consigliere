# Collaudo — prima di consegnare Il Consigliere a un cliente

Gate anti-brutta-figura (deciso con Codex, N389). Spunta tutto su una macchina di prova prima di mostrarlo a un cliente.

## Percorso reale del destinatario

- [ ] Riparti dalla sola email che ricevera' il cliente: non usare la cartella gia' presente sul computer di Sal.
- [ ] Apri link/repo con lo stesso accesso del destinatario. Repo privata senza account autorizzato e verificato = `BLOCCO`.
- [ ] Se il link non e' garantito, prepara un pacchetto allegato autosufficiente e prova davvero download, estrazione e apertura.
- [ ] Dalla cartella ottenuta seguendo l'email, completa installazione e primo collaudo sul sistema operativo previsto.
- [ ] Solo dopo questi controlli l'invio puo' dichiarare `PROVA_DESTINATARIO_OK`.

## Funziona

- [ ] `python3 collector/dossier.py --project "" --top-sample 1` gira senza errori e produce dati (`py` su Windows se serve).
- [ ] `python3 consigliere.py --audience cliente` gira e stampa un messaggio utile, non tecnico.
- [ ] Funziona anche con UN SOLO motore presente (solo Claude o solo Codex): l'altro report dice "non trovato" con eleganza, non crasha.
- [ ] La skill è nella cartella giusta del motore (`.claude/skills/` o `.agents/skills/`).
- [ ] Codex seleziona `SETTIMANA` con `consigliere settimana` o `lancia il consigliere`.
- [ ] Codex seleziona `ADESSO` con `consigliere adesso`, `che dice il Consigliere?` o `valuta questa richiesta con il Consigliere`.
- [ ] Una normale richiesta su email, clienti o file resta fuori dai trigger della skill.
- [ ] Claude espone `/il-consigliere settimana` e `/il-consigliere adesso <richiesta>`; il frontmatter contiene `disable-model-invocation: true`.
- [ ] Lo `SKILL.md` installato punta al `PROCEDURA.md` locale del kit e NON contiene path dell'autore o path di esempio.
- [ ] Genera `docs/tutor/AAAA-Wnn.md` e il file si legge bene in terminale/editor/chat senza segnaposto `{{...}}` rimasti.
- [ ] L'eventuale HTML è solo copia opzionale, non l'output principale.

## Modalità ADESSO

- [ ] Su una richiesta larga restituisce, in 4-10 righe: `Verdetto`, `Causa`, `Prova`, `Prossima azione`.
- [ ] Aggiunge `Prompt migliore` soltanto quando migliora concretamente il risultato.
- [ ] Usa la richiesta corrente come fonte primaria e apre soltanto le fonti necessarie alla prova.
- [ ] In LeaderAI applica l'overlay da `memory/feedback_il_consigliere.md` e `memory/feedback_output_oro.md` quando presenti.
- [ ] Nel kit cliente funziona con `tips_seed.md` e percorsi locali.
- [ ] Crea file o modifica sistemi soltanto quando il comando include anche `applica`, `vai` o `esegui`.
- [ ] Se il bersaglio manca, chiede una sola frase di chiarimento.

## Modalità SETTIMANA

- [ ] Legge i consumi locali con il dossier e mantiene separate le fonti Claude e Codex.
- [ ] Genera il report Markdown in `docs/tutor/AAAA-Wnn.md`.
- [ ] Mantiene l'HTML come copia facoltativa.

## È utile davvero (non solo bello)

- [ ] Il report assomiglia all'output originale: "Dai dati locali...", lista thread pesanti, "Quindi la spiegazione...", "Soluzioni pratiche...".
- [ ] Ci sono 3-5 prove reali (data/peso/modello o cache/titolo), non solo frasi generiche.
- [ ] C'è una frase semplice che interpreta i dati ("il problema è X, non Y").
- [ ] Le soluzioni sono in ordine di impatto e ancorate a conversazioni vere (nome + data + numero), non prediche generiche.
- [ ] Ogni consiglio è azionabile: dice una cosa concreta da fare, non un principio.
- [ ] Ci sono frasi/prompt pronti da copiare.
- [ ] C'è almeno un controllo rapido per verificare da soli il problema.
- [ ] Codex e Claude sono separati chiaramente: chi lancia il report non viene confuso con la fonte dei dati.
- [ ] Se c'è un grafico, è solo supporto dopo il testo; il report resta comprensibile anche senza grafico.
- [ ] C'è un "livello da sbloccare" e non solo la solita lista di consigli.
- [ ] In modalità cliente non compaiono come spiegazione principale termini tecnici tipo `xhigh`, `cache_read`, `token` senza traduzione.
- [ ] Se c'è il report della settimana prima, compare la riga di confronto (meglio/peggio).
- [ ] Se la settimana è pulita, lo dice onestamente invece di inventare problemi.
- [ ] Da nessuna parte si spacciano i token locali per il costo reale: c'è il rimando al pannello ufficiale.

## È sicuro e pulito

- [ ] Zero segreti, token, password o dati personali nel kit.
- [ ] Nessun dato esce dalla macchina (tutto locale).
- [ ] Nel kit non restano path locali dell'autore fuori da esempi interni esplicitamente marcati come LeaderAI.
- [ ] Niente log tecnici nel messaggio finale all'utente.

## Esperienza

- [ ] L'installazione è un solo copia-incolla; l'agente conferma in 3 righe cosa ha fatto.
- [ ] Un non-tecnico capisce il report da solo, senza spiegazioni.
- [ ] Nessuna dashboard/card/grafico decorativo prende spazio alla praticità.
