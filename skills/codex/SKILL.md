---
name: il-consigliere
description: Il Consigliere — coach di efficienza AI con due modalità esplicite. Attivalo soltanto quando l'utente richiama Il Consigliere con "consigliere settimana", "lancia il consigliere", "consigliere adesso", "che dice il Consigliere?" o "valuta questa richiesta con il Consigliere". SETTIMANA analizza i consumi locali di Codex e Claude Code e crea il report in docs/tutor/. ADESSO valuta la richiesta corrente e restituisce verdetto, causa, prova e prossima azione. L'attivazione richiede una delle formule esplicite indicate.
---

Leggi e segui la procedura unica del Consigliere. Ricava dalla richiesta una sola modalità:

- `SETTIMANA`: `consigliere settimana`, `lancia il consigliere`, analisi esplicita dei consumi o attività settimanale;
- `ADESSO`: `consigliere adesso`, `che dice il Consigliere?`, `valuta questa richiesta con il Consigliere`.

Se la formula esplicita è presente e la modalità resta ambigua, chiedi soltanto: `Vuoi il Consigliere SETTIMANA o ADESSO?`

Path procedura: `tools/il-consigliere/PROCEDURA.md` nel workspace corrente.
Se questa skill viene installata da kit su un'altra macchina, l'installatore deve sostituire la riga sopra con il path assoluto locale del `PROCEDURA.md` del kit.

La procedura è la fonte unica delle istruzioni, condivisa con la versione Claude Code. Usa un modello/effort leggero (`medium`).
