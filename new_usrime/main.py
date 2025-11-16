from dotenv import load_dotenv
import os,pandas as pd
import rpy2.robjects as r
from rpy2.robjects import pandas2ri
import rpy2.robjects.packages as rpackages
#from rpy2.robjects.vectors import StrVector
from rpy2.rinterface_lib.embedded import RRuntimeError

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

    r.r(f'png("{PATH}/histograms_crime.png", width=800, height=600); hist(Crime, main="Histogram of Crime", xlab="Crime"); dev.off()')

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
        png("{PATH}/scatterplot_matrix_crime.png", width=800, height=600)
        scatterplotMatrix(~{"+".join(ds.columns.tolist())}, col="black",
            pch=20, regLine = list(method=lm, lty=1, lwd=2, col="chartreuse3"),
            smooth=FALSE,
            diagonal=list(method ="histogram", breaks="FD"),
            main="Matrice di dispersione con rette di regressione",
            data=ds
        )
        dev.off()''')


    m_fors = r.r(f''' 
        library(olsrr)

        model_full <- lm(Crime ~ ., data=ds)
        m_fors <- ols_step_backward_p(model_full)
        
        selected_vars <- m_fors$predictors
        formula_final <- as.formula(paste("Crime ~ .", paste(selected_vars, collapse=" + ")))

        model_final <- lm(formula_final, data=ds)
        summary(model_final)
    ''')

    print(f"Forward Selection Model Summary:\n{m_fors}")

    
    