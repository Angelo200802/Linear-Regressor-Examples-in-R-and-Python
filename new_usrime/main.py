from dotenv import load_dotenv
import os,pandas as pd
import rpy2.robjects as r
from rpy2.robjects import pandas2ri
import rpy2.robjects.packages as rpackages
#from rpy2.robjects.vectors import StrVector
from rpy2.rinterface_lib.embedded import RRuntimeError
import numpy as np

def r_j0(vif_j):
    return {f"Rj0^2_{i}": (1 - 1/vif) for i,vif in zip(vif_j.names,vif_j)}

def install_packages(pckg_names):
    """Install R packages if they are not already installed."""
    
    r.r('''
        options(repos = c(CRAN = "https://cloud.r-project.org"))
    ''')
    
    for pckg in pckg_names:
        if not rpackages.isinstalled(pckg):
            print(f"📦 Installazione di '{pckg}' in corso...")
            
            try:
                # Installa con dipendenze
                result = r.r(f'''
                    tryCatch({{
                        install.packages("{pckg}", dependencies = TRUE, quiet = FALSE)
                        if (require("{pckg}", character.only = TRUE, quietly = TRUE)) {{
                            cat("SUCCESS\n")
                            TRUE
                        }} else {{
                            cat("FAILED\n")
                            FALSE
                        }}
                    }}, error = function(e) {{
                        cat("ERROR:", conditionMessage(e), "\n")
                        FALSE
                    }})
                ''')
                
                # Controlla il risultato
                if result[0]:  # TRUE
                    print(f"✅ Pacchetto '{pckg}' installato con successo!")
                else:
                    print(f"❌ ERRORE: '{pckg}' NON è stato installato!")
                    
            except RRuntimeError as e:
                print(f"❌ ERRORE Python durante l'installazione di '{pckg}':")
                print(f"   {e}")
                
        else:
            print(f"✅ Il pacchetto '{pckg}' è già installato.")
            
        # Verifica finale
        print(f"   Verifica finale: {rpackages.isinstalled(pckg)}")

if __name__ == "__main__":
    load_dotenv()
    PATH = os.getenv("DATASET_PATH")
    DATASET_NAME = "4_New_uscrime_2.txt"

    if PATH is None:
        print("DATASET_PATH is not set in the environment variables.")
        print("Using local path...")
        DATASET_PATH = "./"+DATASET_NAME
    else: 
        DATASET_PATH = PATH+"/"+DATASET_NAME

    install_packages(["DAAG","olsrr","car"])

    ds = r.r(f'''
    df <- read.table(file="{DATASET_PATH}", header=TRUE, sep="\t", dec=",")
    df
    ''')
    r.globalenv['ds'] = ds

    ds : pd.DataFrame = pandas2ri.rpy2py(ds)


    print(f"Dataset:\n{ds}")
    for col,i in zip(ds.columns, range(1,len(ds.columns)+1)):
        c = r.r(f'''
            {col} <- ds[,{i}];
            {col}
        ''')
        r.globalenv[col] = c

    W = r.r(f'''
        W <- cbind({", ".join(ds.columns.tolist())})
        summary(W)
    ''')

    print(f"Matrix W:\n{W}")  

    r.r(f'png("{PATH}/img/histograms_crime.png", width=800, height=600); hist(Crime, main="Histogram of Crime", xlab="Crime"); dev.off()')

    print("Variance and CoVariance Matrix:\n",
          r.r('''
        var_matrix <- var(W)
        var_matrix
    ''')) 

    print("Correlation Matrix:\n",
          r.r('''
        cor_matrix <- cor(W)
        cor_matrix
    '''))

    r.r(f'''
        library(DAAG)
        library(car)
        png("{PATH}/img/scatterplot_matrix_crime.png", width=800, height=600)
        scatterplotMatrix(~{"+".join(ds.columns.tolist())}, col="black",
            pch=20, regLine = list(method=lm, lty=1, lwd=2, col="chartreuse3"),
            smooth=FALSE,
            diagonal=list(method ="histogram", breaks="FD"),
            main="Matrice di dispersione con rette di regressione",
            data=ds
        )
        dev.off()''')

    m = r.r(
        f'''
            model_final <- lm(Crime ~ U2 + M + Po2 + LF , data = ds)

            residuals <- resid(model_final)
            png("{PATH}/img/m_residuals.png", width=800, height=600)
            hist(residuals, main="Histogram of Residuals for Model with break", xlab="Residuals")
            curve(dnorm(x),add=T)

            png("{PATH}/img/m_qqplot.png", width=800, height=600)
            qqnorm(residuals); qqline(residuals)
            dev.off()

            model_final
        '''
    )

    m_complete = r.r(
        f'''
            model_complete <- lm(Crime ~ ., data = ds)
            
            residuals <- resid(model_complete)
            png("{PATH}/img/m_full_residuals.png", width=800, height=600)
            hist(residuals, main="Histogram of Residuals for Model with break", xlab="Residuals")
            curve(dnorm(x),add=T)

            png("{PATH}/img/m_full_qqplot.png", width=800, height=600)
            qqnorm(residuals); qqline(residuals)
            dev.off()

            model_complete
        '''
    )

    det_complete = r.r(''' 
        X <- model.matrix(model_complete)
        det(t(X) %*% X)
    ''')

    det = r.r('''  
        X <- model.matrix(model_final)
        det(t(X) %*% X)
    ''')



    print("Summary of Complete Linear Model:\n",r.r('summary(model_complete)'))
    print("VIF Values for Complete Model:\n",r.r('car::vif(model_complete)'))
    print("Condition Number for Complete Model:\n",r.r('kappa(model.matrix(model_complete))'))
    print("Determinant of X'X for Complete Model:", det_complete)
    print("Rj0 values for Complete Model:\n", r_j0(r.r('car::vif(model_complete)')))
    print("---------------------------------------------------")

    print("Summary of Linear Model:\n",r.r('summary(model_final)'))
    print("VIF Values:\n",r.r('car::vif(model_final)'))
    print("Condition Number:\n",r.r('kappa(model.matrix(model_final))'))
    print("Determinant of X'X:", det)
    print("Rj0 values:\n", r_j0(r.r('car::vif(model_final)')))
    print("---------------------------------------------------")
    
    