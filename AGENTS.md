# Il Consigliere — contratto della repo

Questa è l'unica sorgente del prodotto LeaderAI **Il Consigliere**.
`CLAUDE.md` è il ponte per Claude Code e rimanda a questo file.

## Cosa contiene

- `INSTALLA_CON_AI.md` — percorso di installazione guidato dall'agente.
- `PROCEDURA.md` — istruzioni operative condivise da Claude Code e Codex.
- `collector/` — raccolta locale dei dati di utilizzo, senza inviarli fuori.
- `consigliere.py` — risposta rapida da terminale.
- `skills/` — puntatori da installare per Claude Code e Codex.
- `template_report.md` — formato principale del report.
- `template_report.html` — copia visiva opzionale.
- `tips_seed.md` — catalogo iniziale dei consigli.
- `COLLAUDO.md` — gate obbligatorio prima di una consegna.
- `EMAIL_CONSEGNA.md` — modello unico e versionato per la consegna.
- `IDEE.md` — backlog del prodotto; non è una procedura operativa.

## Regole

1. Una sola repo, una sola fonte: non creare copie fisiche sotto LeaderAI.
2. In LeaderAI `tools/il-consigliere` è soltanto un collegamento a questa repo.
3. Ogni modifica funzionale aggiorna `VERSION` e `CHANGELOG.md`.
4. Prima della consegna eseguire `COLLAUDO.md` partendo dalla sola email del
   destinatario; repo privata non accessibile al cliente = `BLOCCO`.
5. Non inserire token, transcript completi, dati personali o report cliente.
6. I dati locali sono diagnostici: il consumo ufficiale resta quello mostrato
   dai pannelli dei rispettivi servizi.
7. Il report principale è Markdown. L'HTML è soltanto una copia opzionale.

## Prova minima

Da questa cartella:

```bash
python3 collector/dossier.py --project "" --top-sample 1
python3 consigliere.py --audience cliente
```

Se uno dei due motori non è presente, il prodotto deve continuare a funzionare
con l'altro.
