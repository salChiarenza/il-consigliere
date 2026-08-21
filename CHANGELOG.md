# Changelog

## 0.2.0 — 29/07/2026

- Aggiunte le modalità esplicite `SETTIMANA` e `ADESSO` nella procedura unica.
- `SETTIMANA` conserva la diagnosi locale dei consumi e il report Markdown.
- `ADESSO` valuta la richiesta corrente con verdetto, causa, prova e prossima
  azione; aggiunge un prompt migliore quando porta valore.
- Resi stretti i trigger Codex; la skill Claude richiede l'invocazione manuale
  con `disable-model-invocation: true`.
- Aggiunto l'overlay delle regole LeaderAI quando le relative fonti sono
  presenti, mantenendo portabile il kit cliente.

## 0.1.0 — 27/07/2026

- Riunita in questa repo l'unica sorgente fisica del prodotto.
- Aggiunti contratto della repo, versione e modello email di consegna.
- Rinominato l'ingresso in `INSTALLA_CON_AI.md`.
- Conservato il gate del percorso reale del destinatario.
- Eliminata la doppia manutenzione tra sorgente LeaderAI e kit annidato.

La storia precedente del prodotto resta disponibile nella cronologia Git.
