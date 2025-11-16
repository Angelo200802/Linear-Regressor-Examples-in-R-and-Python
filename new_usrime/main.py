from dotenv import load_dotenv
import os,pandas as pd
import rpy2.robjects as r
from rpy2.robjects import pandas2ri

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

    ds = r.r(f'''
    df <- read.table(file="{DATASET_PATH}", header=TRUE, sep="\t", dec=",")
    df
    ''')
    r.globalenv['ds'] = ds

    ds = pandas2ri.rpy2py(ds)

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


    
    