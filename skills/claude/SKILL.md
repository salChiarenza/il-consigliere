---
name: il-consigliere
description: Il Consigliere — coach di efficienza AI con due modalità invocabili dall'utente. Usa `/il-consigliere settimana` per analizzare i consumi locali di Claude Code e Codex e creare il report in docs/tutor/. Usa `/il-consigliere adesso <richiesta>` per ottenere verdetto, causa, prova e prossima azione sulla richiesta corrente.
disable-model-invocation: true
model: sonnet
---

Leggi e segui la procedura unica del Consigliere. Ricava dagli argomenti una sola modalità:

- `SETTIMANA`: `/il-consigliere settimana`;
- `ADESSO`: `/il-consigliere adesso <richiesta>`.

Argomenti ricevuti: `$ARGUMENTS`

Se la modalità resta ambigua, chiedi soltanto: `Vuoi il Consigliere SETTIMANA o ADESSO?`

Path procedura: `tools/il-consigliere/PROCEDURA.md` nel workspace corrente.
Se questa skill viene installata da kit su un'altra macchina, l'installatore deve sostituire la riga sopra con il path assoluto locale del `PROCEDURA.md` del kit.

La procedura è la fonte unica delle istruzioni, condivisa con la versione Codex.
