from dotenv import load_dotenv
import os,pandas as pd
import rpy2.robjects as r
from rpy2.robjects import pandas2ri
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector

def install_packages(package_names):
    """Install R packages if they are not already installed."""
    utils = rpackages.importr('utils')
    utils.chooseCRANmirror(ind=1)  # Select the first CRAN mirror
    for package in package_names:
        if not rpackages.isinstalled(package):
            utils.install_packages(StrVector([package]))
            print(f"📦 Pacchetto '{package}' installato con successo!")
        else:
            print(f"✅ Il pacchetto '{package}' è già installato in R.")

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

    install_packages(['DAAG', 'car'])

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


    
    