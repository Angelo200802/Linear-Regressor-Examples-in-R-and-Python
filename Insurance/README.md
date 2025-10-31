# Progetto di Regressione Lineare - Analisi Dati Assicurativi

## Descrizione del Progetto

Questo progetto implementa un'analisi di regressione lineare per costi assicurativi sanitari utilizzando Python con integrazione R tramite la libreria `rpy2`.

## Dataset

Il dataset `insurance.csv` contiene informazioni su 1338 assicurati con le seguenti variabili:

- **age**: Età dell'assicurato
- **sex**: Sesso (male/female)
- **bmi**: Indice di Massa Corporea (Body Mass Index)
- **children**: Numero di figli a carico
- **smoker**: Stato di fumatore (yes/no)
- **region**: Regione geografica (southwest, southeast, northwest, northeast)
- **charges**: Costi assicurativi (variabile target)

## Obiettivo dell'Analisi

L'obiettivo principale è analizzare la relazione fra diverse variabili indipendenti e i costi assicurativi (variabile dipendente) attraverso un modello di regressione lineare semplice.

## Metodologia

### 1. Caricamento e Esplorazione dei Dati
- Lettura del dataset CSV utilizzando R
- Selezione delle variabili (`x_i`) e costi (`y`)
- Analisi statistiche descrittive (summary, varianza, correlazione)

### 2. Visualizzazioni
Il progetto genera due visualizzazioni principali:

- **`hist_charges.png`**: Istogramma della distribuzione dei costi assicurativi
- **`scatter_bmi_charges.png`**: Scatter plot che mostra la relazione tra BMI e costi assicurativi

### 3. Modello di Regressione Lineare
- Implementazione di un modello di regressione lineare: `charges ~ bmi`
- Valutazione del modello attraverso il summary statistico

## Struttura del Progetto

```
├── README.md                    # Documentazione del progetto
├── insurance.csv               # Dataset originale
├── m1.py                      # Script principale di analisi
├── hist_charges.png           # Istogramma dei costi assicurativi
└── scatter_bmi_charges.png    # Scatter plot BMI vs Costi
```

## Come Eseguire il Progetto

1. Assicurarsi di avere installato:
   - Python 3.x
   - R
   - Dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

2. Eseguire lo script principale:
   ```bash
   python m1.py
   ```

3. I risultati includeranno:
   - Statistiche descrittive stampate in console
   - Risultati del modello di regressione
   - Grafici salvati come file PNG

## Risultati Ottenuti per M1

### Statistical Summary of Variables
       y               x1       
 Min.   : 1122   Min.   :15.96  
 1st Qu.: 4740   1st Qu.:26.30  
 Median : 9382   Median :30.40  
 Mean   :13270   Mean   :30.66  
 3rd Qu.:16640   3rd Qu.:34.69  
 Max.   :63770   Max.   :53.13  

### Variance of Variables
             y          x1
y  146652372.2 14647.30443
x1     14647.3    37.18788

### Correlation index between Variables
          y       x1
y  1.000000 0.198341
x1 0.198341 1.000000

### Summary of Linear Model M1

lm(formula = y ~ x1)

Residuals:
   Min     1Q Median     3Q    Max 
-20956  -8118  -3757   4722  49442 

Coefficients:
            Estimate Std. Error t value Pr(>|t|)    
(Intercept)  1192.94    1664.80   0.717    0.474    
x1            393.87      53.25   7.397 2.46e-13 ***
---

Residual standard error: 11870 on 1336 degrees of freedom
Multiple R-squared:  0.03934,   Adjusted R-squared:  0.03862 
F-statistic: 54.71 on 1 and 1336 DF,  p-value: 2.459e-13


*La varianza spiegata dal modello è solo del 3.93, è dunque un modello debole.*

*Per ogni aumento di 1 unità di BMI, le charges aumentano in media di ~394 dollari*

## Note

Progetto di test sviluppato per il corso Modelli Statistici e Statistical Learning

