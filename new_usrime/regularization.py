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
        model_withe <- lm(res2 ~ fit1 + fit1_2)
    ''')
    #lambda=lambda_grid
    ridge = r.r(f'''
        library(glmnet)
        set.seed(123)
        lambda_grid <- 10^seq(10, -10, length = 200)
        X_matrix <- as.matrix(ds[ , !(names(ds) %in% c("Crime")) ])
        y_vector <- as.vector(ds$Crime)
        ridge_model <- cv.glmnet(X_matrix, y_vector, alpha=1, nfolds = 5, lambda = lambda_grid)
        
        png("{PATH}/img/ridge_path_plot.png", width=800, height=600)
        plot(ridge_model, label=TRUE)
        dev.off()        
        best_lambda <- ridge_model$lambda.min
        best_lambda
    ''')

    best_lambda = r.r(f'''
        set.seed(123)
        best_ridge <- glmnet(X_matrix, y_vector,lambda=best_lambda, nfolds = 5, alpha=1)
        best_ridge
    ''')

    print(f"Ridge Regression - Optimal Lambda: {ridge}")
    print("Ridge MSE:\n", r.r('best_ridge$lambda.1se'))
    print("Ridge Regression Coefficients:\n", r.r('coef(best_ridge)'))
    #print("Linear Model Summary:\n", r.r('summary(model)'))
    #print("Breusch-Pagan Test Summary:\n", r.r('summary(fit2)'))
    #print("White Test Summary:\n", r.r('summary(model_withe)'))
