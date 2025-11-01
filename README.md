# Progetto di Regressione Lineare - Analisi Dati Assicurativi

## Obiettivo Principale

Questo progetto implementa un'analisi di regressione lineare per studiare la relazione tra diverse variabili demografiche e sanitarie (età, BMI, stato di fumatore, ecc.) e i costi assicurativi sanitari. L'analisi utilizza Python con integrazione R tramite la libreria `rpy2` per esplorare come i fattori individuali influenzano i costi delle polizze assicurative.

Il dataset contiene informazioni su 1338 assicurati e permette di sviluppare modelli predittivi per stimare i costi assicurativi basati su caratteristiche personali e sanitarie.

## Struttura del Progetto

```
├── README.md                    # Documentazione generale del progetto
├── Insurance/                   # Cartella principale dell'analisi
│   ├── insurance.csv           # Dataset originale
│   ├── m1.py                   # Modello 1: Regressione BMI vs Charges
│   ├── m2.py                   # Modello 2: Analisi multivariata
│   ├── m1.md                   # Documentazione dettagliata Modello M1
│   ├── hist_charges.png        # Istogramma distribuzione costi
│   ├── m1_scatter_plot.png     # Scatter plot BMI vs Charges
│   ├── m1_residuals.png        # Analisi dei residui M1
│   └── requirements.txt        # Dipendenze Python
```

## Installazione e Setup Locale

### Prerequisiti

Assicurarsi di avere installato sul sistema:
- **Python 3.7+**
- **R 4.0+**
- **Git** (per clonare il repository)

### Installazione delle Dipendenze Python

1. **Clonare il repository** (se applicabile):
   ```bash
   git clone <repository-url>
   cd ms_sl_ws
   ```

2. **Creare un ambiente virtuale Python** (raccomandato):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # oppure
   venv\Scripts\activate     # Windows
   ```

3. **Installare le dipendenze Python**:
   ```bash
   cd Insurance
   pip install -r requirements.txt
   ```

### Installazione delle Dipendenze R

Le principali librerie R utilizzate sono:
- Base R (per statistiche e grafici)
- Eventuali pacchetti aggiuntivi specificati nei singoli script

### Esecuzione del Progetto

Per eseguire l'analisi del **Modello M1** (BMI vs Charges):
```bash
cd Insurance
python m1.py
```

Per eseguire l'analisi del **Modello M2** (analisi multivariata):
```bash
cd Insurance
python m2.py
```

### Output Generati

L'esecuzione degli script produrrà:
- **Statistiche descrittive** stampate in console
- **Risultati dei modelli di regressione** con parametri e test statistici
- **Grafici salvati come file PNG** nella cartella Insurance

### Risoluzione Problemi Comuni

1. **Errore rpy2**: Verificare che R sia installato e nel PATH del sistema
2. **Errore pacchetti Python**: Assicurarsi che l'ambiente virtuale sia attivato
3. **Errore lettura CSV**: Verificare che il file `insurance.csv` sia presente nella cartella Insurance

## Documentazione Dettagliata

Per analisi approfondite e risultati specifici, consultare:
- **`Insurance/m1.md`**: Documentazione completa del Modello M1 con tutti i risultati statistici
- **`Insurance/m2.md`**: Documentazione del Modello M2 (se disponibile)

## Note

Progetto sviluppato per il corso **Modelli Statistici e Statistical Learning** - Anno Accademico 2024/2025

