# Il Consigliere

**Efficacia & Efficienza**, il coach LeaderAI che migliora una richiesta nel
momento in cui nasce e trasforma i dati locali dell'uso di Claude Code e Codex
in poche correzioni pratiche.

Questa è l'unica repo del prodotto. La cartella visibile dentro LeaderAI è un
collegamento alla stessa sorgente fisica.

## Cosa fa

Il Consigliere ha due modalità:

- **ADESSO**: valuta la richiesta corrente e restituisce verdetto, causa, prova
  e prossima azione;
- **SETTIMANA**: mostra quali conversazioni hanno pesato davvero, spiega il
  motivo in italiano semplice e propone cosa fare nel lavoro successivo.

Il report settimanale principale è Markdown.

Esempi:

- una conversazione conteneva lavori diversi e andava divisa;
- un modello pesante è stato usato per un compito semplice;
- una richiesta troppo larga ha costretto l'agente a rileggere troppo contesto.

## Privacy

Lavora in locale sui dati che Claude Code e Codex hanno già salvato sul
computer. Non invia transcript o dati di utilizzo all'esterno. I dati locali
servono alla diagnosi; il conteggio ufficiale resta quello del pannello del
servizio.

## Installazione

Apri [`INSTALLA_CON_AI.md`](INSTALLA_CON_AI.md) con Claude Code o Codex.
L'agente rileva l'ambiente, installa la skill corretta, esegue il primo test e
riporta ciò che funziona e gli eventuali blocchi umani.

Prima di consegnarlo a un cliente va completato
[`COLLAUDO.md`](COLLAUDO.md), partendo dalla sola email che riceverà il
destinatario.

## Uso

- Codex: scrivi **"consigliere adesso: [richiesta]"** oppure
  **"consigliere settimana"**.
- Claude Code: usa **`/il-consigliere adesso [richiesta]`** oppure
  **`/il-consigliere settimana`**.
- **"lancia il consigliere"** continua ad avviare la modalità SETTIMANA.
- Da terminale: `python3 consigliere.py --audience cliente`.
- Raccolta dati: `python3 collector/dossier.py --project "" --top-sample 3`.

Il report principale viene creato in `docs/tutor/AAAA-Wnn.md`. La copia HTML è
opzionale.

## Struttura

La mappa completa è in [`AGENTS.md`](AGENTS.md). La versione corrente è in
[`VERSION`](VERSION); le modifiche sono registrate in
[`CHANGELOG.md`](CHANGELOG.md).
