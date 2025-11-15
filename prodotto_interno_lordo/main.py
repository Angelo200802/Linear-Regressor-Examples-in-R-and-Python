from dotenv import load_dotenv
import os,pandas as pd
import rpy2.robjects as r
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector

if __name__ == "__main__":
    load_dotenv()
    PATH = os.getenv("DATASET_PATH")
    DATASET_NAME = "Prodotto interno lordo Dati Trimestrali _ ISTAT.xlsx"

    if PATH is None:
        print("DATASET_PATH is not set in the environment variables.")
        print("Using local path...")
        DATASET_PATH = DATASET_NAME
    else: 
        DATASET_PATH = PATH+"/"+DATASET_NAME

    # Verifica se 'tseries' è installato
    if rpackages.isinstalled('tseries'):
        print("✅ Il pacchetto 'tseries' è installato in R.")
    else:
        utils = rpackages.importr('utils')
        utils.chooseCRANmirror(ind=1)
        utils.install_packages(StrVector(['tseries']))
        print("📦 Pacchetto 'tseries' installato con successo!")
    
    df = r.r(f'''
        library(readxl)
library(dplyr)

df <- read_excel("{DATASET_PATH}", skip = 7, col_names = FALSE)
df <- df %>% filter(!if_all(-1, is.na))
valori <- df[2, -1] %>% unlist()
valori <- as.numeric(gsub(",", ".", trimws(valori)))
valori <- valori[!is.na(valori)]
ts_pil <- ts(valori, start = c(1996, 1), frequency = 4)
ts_pil
    ''')

    r.globalenv['ts_pil'] = df

    r.r(f'''
        png("{PATH}/serie_trimestrale.png", width=800, height=600)
        plot(ts_pil, main="Serie Trimestrale del Prodotto Interno Lordo", ylab="PIL", xlab="Anno", col="blue")
        dev.off()
    ''')

    m = r.r('''
        t <- seq(1, length(ts_pil),1)
        m <- lm(ts_pil ~ poly(t,3,raw=TRUE))
        summary(m)
    ''')

    m_dummy = r.r('''
        t <- 1:length(ts_pil) #1-118
        time_points <- time(ts_pil)
        
        dummy_08 <- ifelse(time_points >= 2008.00, 1, 0)
        dummy_20 <- ifelse(time_points >= 2020.00, 1, 0)
                  
        m <- lm(ts_pil ~ poly(t,3,raw=TRUE) + dummy_08 + dummy_20)
        summary(m)
    ''')

    print("DATASET:\n", df)

    print("Summary of Linear Model M (no break):\n",m)

    print("Summary of Linear Model M (with breaks):\n",m_dummy)