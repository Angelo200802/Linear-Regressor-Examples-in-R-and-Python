from dotenv import load_dotenv
import os
import rpy2.robjects as r
from main import load_dataset, install_packages

if __name__ == "__main__":
    load_dotenv()
    PATH = os.getenv("DATASET_PATH")
    DATASET_NAME = "4_New_uscrime_2.txt"

    install_packages(["glmnet"])
    
    ds = load_dataset(PATH, DATASET_NAME)

    for col,i in zip(ds.columns, range(1,len(ds.columns)+1)):
        c = r.r(f'''
            {col} <- ds[,{i}];
            {col}
        ''')
        r.globalenv[col] = c

    # Separazione delle features e target
    X = ds[[c for c in ds.columns if c != "Crime"]]
    y = ds["Crime"]

    model = r.r('''
        model <- lm(Crime ~ ., data=ds)
        model                
    ''')

    resid = r.r(f'''
        fit <- fitted(model)
        res <- resid(model)
        png("{PATH}/img/res_plot.png", width=800, height=600)
        plot(fit,res)
        dev.off()

    ''')

    breusch_pagan = r.r('''
        res2 <- resid(model)^2
        fit2 <- lm(res2 ~ ., data=ds)
        fit2
    ''')

    white_test = r.r('''
        fit1 <- fitted(model)
        fit1_2 <- fit1^2
        res2 <- resid(model)^2
        model_white <- lm(res2 ~ fit1 + fit1_2)
        model_white
    ''')

    for c in ds.columns:
        wt_c = r.r(f'''
            {c}_wt <- {c}/fitted(model)
        ''')

    wt_model = r.r(f"""
        fit1_r <- 1/fitted(model)
        wt_estimate <- lm(Crime_wt ~ fit1_r + {"+".join([c+"_wt" for c in ds.columns if c != "Crime" and c != "Time" and c!= "Ed" and c !="Wealth"])} -1)
        wt_estimate
    """)
    
    print("Summary BP: \n",r.r("summary(fit2)"))
    print("Summary WT: \n",r.r("summary(model_white)"))
    print("Summary WT Estimation: \n",r.r("summary(wt_estimate)"))