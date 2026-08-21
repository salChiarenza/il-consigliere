# Idee prodotto — Il Consigliere

Questo file tiene le idee vive del prodotto, senza trasformarle subito in feature.
La procedura operativa resta `PROCEDURA.md`; qui si salva la direzione.

## Principio madre

Il Consigliere non deve essere una dashboard. Deve essere una risposta utile:

1. dati locali;
2. lista delle conversazioni pesanti;
3. spiegazione semplice;
4. soluzioni pratiche;
5. eventuale mini-grafico solo dopo, come supporto visivo.

## Cliente: traduzione, non tecnica

Il cliente non deve capire `token`, `xhigh`, `cache_read`, `reasoning` o `thread`.
Quella è lingua interna.

Il Consigliere deve tradurre così:

| Interno | Cliente |
|---|---|
| token / consumo | lavoro pesante per l'AI |
| cache_read / contesto trascinato | conversazione troppo lunga che l'AI deve rileggere |
| reasoning xhigh | modalità di ragionamento pesante |
| thread-mostro | conversazione diventata troppo grande |
| perimetro largo | richiesta troppo ampia |

Frase guida:

> Se cambia il verbo, cambia chat.

Esempio cliente:

```text
Questa settimana hai usato la stessa conversazione per analizzare, scrivere e correggere.
Qui l'AI ha dovuto portarsi dietro troppe cose.
La prossima volta: una conversazione per analizzare, una nuova per scrivere.
```

## Livelli da sbloccare

Il Consigliere non deve ripetere sempre "apri chat nuova" o "usa meno modello pesante".
Deve far crescere l'utente.

### Livello 1 — Spegni sprechi evidenti

Obiettivo: evitare conversazioni enormi e richieste troppo larghe.

Segnali:
- stessa chat usata per molti lavori;
- richiesta tipo "controlla tutto";
- modello pesante usato per task semplici.

### Livello 2 — Prompt più stretti

Obiettivo: insegnare all'utente a dare fonte, perimetro e formato.

Frase pronta:

```text
Leggi solo questi file. Dammi causa, prova e prossima azione.
```

### Livello 3 — Cambi fase bene

Obiettivo: separare analisi, decisione, scrittura, modifica e collaudo.

Regola cliente:

```text
Se cambia il verbo, cambia chat.
```

### Livello 4 — Procedure riusabili

Obiettivo: quando una cosa si ripete, non rifarla in chat: diventa procedura, template o skill.

### Livello 5 — Prevenzione

Obiettivo: Il Consigliere interviene prima dello spreco:

```text
Questa richiesta è troppo larga. Spezzala così...
```

## Come deve cambiare il report nel tempo

Ogni report dovrebbe contenere:

```text
Cosa hai già migliorato
Cosa non ti ripeto più
Nuovo livello da sbloccare
Mossa della settimana
```

Questo evita l'effetto noia: il Consigliere non è una sveglia che ripete, è un coach che aumenta il livello.
