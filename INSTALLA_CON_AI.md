# Installazione con l'agente — Il Consigliere
**Efficacia & Efficienza** · LeaderAI

Apri questa repo con **Claude Code o Codex** e chiedi all'agente di eseguire la
missione seguente. L'agente fa diagnosi, installazione e collaudo; il
proprietario interviene soltanto per permessi, accessi e scelte reali.

> Funziona uguale sui due motori: il prompt capisce da solo se è Claude o Codex e installa la parte giusta. Tutto resta **in locale sul tuo computer** — nessun dato esce, nessun account da collegare.

---

## Missione di installazione

```
Sei l'installatore de "Il Consigliere", un coach di efficienza per l'uso dell'AI. Sei dentro la cartella del kit. Installa così, senza inventare nulla fuori da questi file:

1. FISSA LA CASA. Usa come `CONSIGLIERE_ROOT` la cartella assoluta di questo kit. Se l'utente vuole spostarlo in una posizione stabile, fallo adesso e poi aggiorna `CONSIGLIERE_ROOT`. Da qui in poi non usare path di esempio.

2. CAPISCI CHI SEI. Se giri in Claude Code, la tua skill va in `.claude/skills/il-consigliere/`. Se giri in Codex, va in `.agents/skills/il-consigliere/`. Crea la cartella giusta e copiaci `skills/claude/SKILL.md` (Claude) o `skills/codex/SKILL.md` (Codex) come `SKILL.md`.

3. PUNTA LA PROCEDURA GIUSTA. Nel `SKILL.md` appena copiato, sostituisci la riga `Path procedura:` con il path assoluto locale:
   `Path installazione: <CONSIGLIERE_ROOT>/PROCEDURA.md`.
   La skill deve leggere il `PROCEDURA.md` di questa installazione, non un path dell'autore o un path di esempio.

4. METTI A POSTO IL MOTORE. Lascia `collector/` (dossier.py, claude_usage.py, codex_usage.py), `template_report.html`, `PROCEDURA.md` e `README.md` dentro `CONSIGLIERE_ROOT`. Non separare questi file: la procedura li usa come blocco unico.

5. SEME DEI CONSIGLI. Se non esiste già `memory/reference_consigliere_tips.md` nel workspace dell'utente, crea `memory/` se serve e copia `tips_seed.md` lì come punto di partenza del catalogo condiviso.

6. COLLAUDA SUBITO (PASSO obbligatorio). Esegui `python3 collector/dossier.py --project "" --top-sample 1` dalla cartella `CONSIGLIERE_ROOT` e verifica che produca dati senza errori. Se `python3` non esiste e sei su Windows, prova `py`. Se manca un motore (solo Claude o solo Codex), deve comunque funzionare con l'altro.

7. PROVA LE DUE MODALITÀ.
   - ADESSO: valuta una richiesta larga di prova e verifica che l'output contenga
     `Verdetto`, `Causa`, `Prova` e `Prossima azione`.
   - SETTIMANA: esegui la procedura per la settimana corrente e genera il primo
     report in `docs/tutor/AAAA-Wnn.md` dentro il workspace dell'utente.
   Mostra il report all'utente; genera l'HTML soltanto se lo richiede.

8. CONTROLLO ANTI-BRUTTA-FIGURA. Prima di chiudere, verifica:
   - nello `SKILL.md` installato non resta un path dell'autore o un path di esempio;
   - nel report non restano segnaposto `{{...}}`;
   - il messaggio finale non contiene log tecnici.

9. (OPZIONALE) SETTIMANALE. Se l'utente vuole il report automatico ogni lunedì mattina, crea un'attività schedulata che esegua `PROCEDURA.md`, con modello leggero.

Alla fine di' all'utente, in 3 righe: cosa hai installato, come si lanciano
`ADESSO` e `SETTIMANA`, e dove trova il report. Niente log tecnici.
```

---

Dopo l'installazione usi `ADESSO` per migliorare una richiesta e `SETTIMANA`
per la revisione dei consumi. L'eventuale automazione continua a generare la
revisione settimanale.
