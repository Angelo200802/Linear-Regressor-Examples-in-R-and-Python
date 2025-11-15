from dotenv import load_dotenv
import os,pandas as pd
import rpy2.robjects as r

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