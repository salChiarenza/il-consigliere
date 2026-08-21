---
name: reference_consigliere_tips
description: "Catalogo condiviso dei tips di efficienza AI — lo leggono e lo aggiornano sia la versione Claude sia la versione Codex de \"Il Consigliere\". Una fonte, due motori."
metadata: 
  node_type: memory
  trigger: "consigliere, tips efficienza, consumo, contesto, perimetro, xhigh, cache_read"
  type: reference
  originSessionId: 53e3f1d0-a906-4f01-bf5c-c1efd879c65f
---

# Catalogo tips de Il Consigliere (condiviso Claude + Codex)

Fonte unica dei consigli di efficienza. Entrambe le versioni del Consigliere (Claude e Codex) **leggono questo file** quando scrivono il report settimanale e **vi aggiungono** ogni pattern nuovo che scoprono analizzando le chat. Così Codex migliora la sua versione con quello che impara Claude e viceversa. Principio madre: [[feedback_economia_contesto]] — il costo sta nell'input/contesto trascinato, non nell'output.

## Comuni (valgono per Claude e Codex)

1. **Chat nuova per ogni task/cliente grosso.** È la leva regina: un thread lungo ripaga tutto il contesto a ogni turno.
2. **Perimetro esplicito.** Dire file/cartelle precise ("solo `commerciale/<cliente>`, STATUS + proposta"), mai "il workspace".
3. **Modello/effort calibrato al peso.** Leggero per recap/controlli/piccole modifiche; pesante solo per costruire, decidere, architettura, debug duro.
4. **Diagnosi prima dell'azione sui task larghi.** Prima dire quali fonti/file si leggerebbero e cosa si evita; poi agire.
5. **Materializzare in `.md` i file pesanti riletti spesso** (MarkItDown) invece di rileggere PDF/DOCX nativi a ogni giro.
6. **L'output corto NON è la leva.** Il testo prodotto è ~1% del costo: non sprecare tempo ad accorciare le risposte.
7. **Dato vero -> significato -> mossa.** Il report deve prima mostrare 3-5 prove reali, poi spiegare cosa significano in una frase semplice, poi dare poche mosse utili.
8. **Utile e utilizzabile batte estetica.** Ogni report deve includere frasi pronte da copiare e un controllo rapido; senza un'azione immediata non è un consiglio.
9. **Formato originale prima di tutto.** Output principale in testo/Markdown: "Dai dati locali..." -> lista thread -> spiegazione probabile -> soluzioni pratiche. HTML solo copia opzionale.
10. **Separare fonte e motore.** Codex locale e Claude locale sono fonti diverse; chi lancia il Consigliere non è la fonte dei dati.
11. **Grafico dopo, non al posto.** Un mini-grafico in chat può aiutare chi è visivo, ma solo dopo il testo che spiega il problema.
12. **Traduci per il cliente.** Interno: token, xhigh, cache_read. Cliente: conversazione lunga, richiesta ampia, lavori mescolati, AI che rilegge troppe cose.
13. **Se cambia il verbo O il dominio, cambia chat.** Analizzare, scrivere, correggere, decidere e collaudare sono fasi diverse; ma anche dentro una sessione di dettatura continua, argomenti scollegati (es. debug di un prodotto → trattativa auto → amministrazione) sono mondi diversi: la chat va chiusa al primo, non solo quando cambia la fase dello stesso progetto (visto 02-03/07: Voce + acquisto auto nella stessa chat da 201M token).
14. **Livelli, non ripetizione.** Quando l'utente ha imparato una cosa, il report deve dire "non te lo ripeto più" e proporre il livello successivo.
15. **Se il primo giro non convince, stringi — non rilanciare.** Riaprire lo stesso prompt in un thread nuovo ripaga tutto il contesto da capo; nello stesso thread si restringe il perimetro ("guarda SOLO [pezzo], max 5 correzioni"). Visto 10-11/07/2026: revisione sito .ai rilanciata 10+ volte su ultra ≈ 520M token.
16. **Report scansionabile.** Bullet point, righe corte, emoji fisse come segnaposto di sezione (🧭 ⚡ 📊 🔍 💡 ✅ 🤐 🔓 🛠️ 📋 🔎 📈), apertura "⚡ In una riga", 🟢/🔴 sui numeri. Facile da consultare a colpo d'occhio (richiesta Sal 14/07/2026; esempio-modello `docs/tutor/2026-W29.md`). Vale in aggiunta al formato originale del tip 9.

## Solo Claude Code

- **cache_read ≈ 95% del consumo.** Il nemico è la chat lunga, non la risposta lunga. La diagnosi sta in `tools/claude-usage/report.py` (colonna cache_r).
- **Opus pesa ~9× Sonnet** (per volume osservato). Default Sonnet; Opus solo per costruire/decidere.

## Solo Codex

- **`xhigh` ≈ 65% della spesa.** Tienilo per architettura/debug/decisioni complesse; `medium`/`low` per il resto. Diagnosi in `tools/codex-usage/report.py` (colonna model/effort).
- **L'effort si sistema nel config, non nel prompt.** `model_reasoning_effort` in `~/.codex/config.toml` (e nei `.codex/config.toml` di progetto) è il default di OGNI thread: se lì c'è `xhigh`, dire "usa medium" nel prompt non basta. La leva strutturale è mettere `medium` nel config e chiedere il pesante solo quando serve (scoperto 14/07/2026: xhigh cablato in entrambi i config → effort alto al 99%).

## Come si aggiorna

Quando un Consigliere, analizzando le chat della settimana, trova un pattern di spreco ricorrente non ancora elencato qui, aggiunge una riga nella sezione giusta (Comuni / Claude / Codex) con una formulazione breve e azionabile. Niente doppioni: se il tip esiste già, si affina quello. Le scoperte nuove e stabili che cambiano il metodo vanno anche promosse in [[feedback_economia_contesto]].
