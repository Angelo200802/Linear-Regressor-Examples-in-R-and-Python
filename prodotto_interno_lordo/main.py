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

    xx = r.r('''
    yy <- rep(c(1,2,3,4),31)
    xx <- yy[1:length(ts_pil)]
    xx
''')
    
    r.globalenv['xx'] = xx

    pil = r.r("""
    d1 <- ifelse(xx == 1, 1, 0)
    d2 <- ifelse(xx == 2, 1, 0)
    d3 <- ifelse(xx == 3, 1, 0)
    d4 <- ifelse(xx == 4, 1, 0)
    pil_ds <- cbind(xx,ts_pil)
    pil <- cbind(xx,ts_pil,d1,d2,d3,d4)
    pil
""")

    m = r.r(f'''
        t <- seq(1, length(ts_pil),1) 
        d1 <- ifelse(xx == 1, 1, 0)
        d2 <- ifelse(xx == 2, 1, 0)
        d3 <- ifelse(xx == 3, 1, 0)
        d4 <- ifelse(xx == 4, 1, 0) 
        m <- lm(ts_pil ~ d1+d2+d3+d4+poly(t,3,raw=TRUE)-1)
            
        png("{PATH}/time_series_comparison_no_break.png", width=1200, height=600)
        fitted_ts <- ts(fitted(m), start=start(ts_pil), frequency=frequency(ts_pil))
        ts.plot(fitted_ts, ts_pil, gpars=list(col=c(2,3)), main="Observed vs Fitted Values (no break)")
        
        legend("topleft", 
            legend=c("Fitted", "Observed"), 
            col=c("red", "green"), 
            lty=c(2, 1), 
            lwd=2)

        png("{PATH}/m_residuals.png", width=800, height=600)
        hist(resid(m), main="Histogram of Residuals for Model without break", xlab="Residuals")
        
        dev.off()
        summary(m)
    ''')
    
    m_dummy = r.r(f'''
        t <- 1:length(ts_pil) #1-118
        time_points <- time(ts_pil)
        
        d1 <- ifelse(xx == 1, 1, 0)
        d2 <- ifelse(xx == 2, 1, 0)
        d3 <- ifelse(xx == 3, 1, 0)
        d4 <- ifelse(xx == 4, 1, 0)           
        dummy_08 <- ifelse(time_points >= 2008.00, 1, 0)
        dummy_20 <- ifelse(time_points >= 2020.00, 1, 0)
                  
        model_full <- lm(ts_pil ~ d1+d2+d3+d4+poly(t, 1, raw = TRUE) + dummy_08 + dummy_20 + dummy_08:t + dummy_20:t -1)
        
        png("{PATH}/time_series_comparison.png", width=1200, height=600)
        fitted_ts <- ts(fitted(model_full), start=start(ts_pil), frequency=frequency(ts_pil))
        ts.plot(fitted_ts, ts_pil, gpars=list(col=c(2,3)), main="Observed vs Fitted Values")
        
        legend("topleft", 
            legend=c("Fitted", "Observed"), 
            col=c("red", "green"), 
            lty=c(2, 1), 
            lwd=2)

        png("{PATH}/m_full_residuals.png", width=800, height=600)
        hist(resid(model_full), main="Histogram of Residuals for Model with break", xlab="Residuals")

        dev.off()
        summary(model_full)
    ''')

    r.globalenv['model_full'] = m_dummy

    #m_tratto_1= r.r('''
    #    periodo1 <- window(ts_pil, end = c(2007, 4))    # 1996-2007
    #    t1 <- 1:length(periodo1)
    #    model1 <- lm(periodo1 ~ poly(t1, 1, raw = TRUE))
    #    summary(model1)
    #''')

    #m_tratto_2 = r.r(
    #    '''
    #    periodo2 <- window(ts_pil, start = c(2008, 1), end = c(2019, 4))  # 2008-2019
    #    t2 <- 1:length(periodo2)
    #    model2 <- lm(periodo2 ~ 1)
    #    summary(model2)   
    #    '''
    #)

    #m_tratto_3 = r.r(
    #    '''
    #    periodo3 <- window(ts_pil, start = c(2020, 1))  # 2020-oggi
    #    t3 <- 1:length(periodo3)
    #    model3 <- lm(periodo3 ~ poly(t3, 2, raw = TRUE))  # Meno dati, polinomio più basso
    #    summary(model3)
    #    '''
    #)

    print("DATASET:\n", df)

    print("Summary of Linear Model M (no break):\n",m)

    print("Summary of Linear Model M (with breaks):\n",m_dummy)

    #print("Summary of Linear Model for Segment 1 (1996-2007):\n",m_tratto_1)
    #print("Summary of Linear Model for Segment 2 (2008-2019):\n",m_tratto_2)
    #print("Summary of Linear Model for Segment 3 (2020-present):\n",m_tratto_3)