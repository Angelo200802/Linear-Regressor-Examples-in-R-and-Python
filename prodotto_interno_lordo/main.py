from dotenv import load_dotenv
import os
import rpy2.robjects as r
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector

if __name__ == "__main__":
    load_dotenv()
    PATH = os.getenv("DATASET_PATH")
    DATASET_NAME = "Prodotto interno lordo Dati Trimestrali _ ISTAT.xlsx"

    if PATH is None:
        print("DATASET_PATH is not set in the environment variables.")
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
        read_excel("{DATASET_PATH}", skip = 8)
    ''')

    print(df)