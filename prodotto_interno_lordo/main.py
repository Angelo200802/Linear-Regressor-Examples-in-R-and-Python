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
        png("{PATH}/img/serie_trimestrale.png", width=800, height=600)
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
    
    m_trend = r.r(f''' 
        t <- seq(1, length(ts_pil),1)
        m_trend <- lm(ts_pil ~ poly(t, 3, raw=TRUE))
                  
        png("{PATH}/img/m_trend.png", width=800, height=600)
        fitted_trend <- fitted(m_trend)
        ts.plot(fitted_trend, ts_pil, gpars=list(col=c(2,3)), main="Observed vs Fitted Values (Trend Only)")
        dev.off()
        m_trend
    ''')

    m = r.r(f'''
        t <- seq(1, length(ts_pil),1) 
        d1 <- ifelse(xx == 1, 1, 0)
        d2 <- ifelse(xx == 2, 1, 0)
        d3 <- ifelse(xx == 3, 1, 0)
        d4 <- ifelse(xx == 4, 1, 0) 
        m <- lm(ts_pil ~ d1+d2+d3+d4+poly(t,3,raw=TRUE)-1)
            
        png("{PATH}/img/time_series_comparison_no_break.png", width=1200, height=600)
        fitted_ts <- ts(fitted(m), start=start(ts_pil), frequency=frequency(ts_pil))
        ts.plot(fitted_ts, ts_pil, gpars=list(col=c(2,3)), main="Observed vs Fitted Values (no break)")
        
        legend("topleft", 
            legend=c("Fitted", "Observed"), 
            col=c("red", "green"), 
            lty=c(2, 1), 
            lwd=2)

        residuals <- resid(m)

        png("{PATH}/img/m_residuals.png", width=800, height=600)
        hist(residuals, main="Histogram of Residuals for Model without break", xlab="Residuals")
        
        png("{PATH}/img/m_qqplot.png", width=800, height=600)
        qqnorm(residuals); qqline(residuals)

        dev.off()
        m
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
                  
        model_full <- lm(ts_pil ~ d1+d2+d3+d4+poly(t, 3, raw = TRUE) + dummy_08+ dummy_08:t + dummy_20 -1)
        
        png("{PATH}/img/time_series_comparison.png", width=1200, height=600)
        fitted_ts <- ts(fitted(model_full), start=start(ts_pil), frequency=frequency(ts_pil))
        ts.plot(fitted_ts, ts_pil, gpars=list(col=c(2,3)), main="Observed vs Fitted Values")
        
        legend("topleft", 
            legend=c("Fitted", "Observed"), 
            col=c("red", "green"), 
            lty=c(2, 1), 
            lwd=2)

        residuals <- resid(model_full)
            
        png("{PATH}/img/m_full_residuals.png", width=800, height=600)
        hist(residuals, main="Histogram of Residuals for Model with break", xlab="Residuals")
        curve(dnorm(x),add=T)

        png("{PATH}/img/m_full_qqplot.png", width=800, height=600)
        qqnorm(residuals); qqline(residuals)
        dev.off()
        
        model_full
    ''')

    r.globalenv['model_full'] = m_dummy
    r.globalenv['model_no_break'] = m
    r.globalenv['model_trend'] = m_trend

    print("DATASET:\n", df)

    print("Summary of Linear Model M_trend:\n",r.r('summary(model_trend)'))

    print("Summary of Linear Model M (no break):\n",r.r('summary(model_no_break)'))

    print("Summary of Linear Model M (with breaks):\n",r.r('summary(model_full)'))  

    print("AIC of M_trend:", r.r('AIC(model_trend)'))
    print("AIC of M (no break):", r.r('AIC(model_no_break)'))
    print("AIC of M (with breaks):", r.r('AIC(model_full)'))
    print("BIC of M_trend:", r.r('BIC(model_trend)'))
    print("BIC of M (no break):", r.r('BIC(model_no_break)'))
    print("BIC of M (with breaks):", r.r('BIC(model_full)')) 