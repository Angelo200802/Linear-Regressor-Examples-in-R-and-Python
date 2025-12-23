from dotenv import load_dotenv
import os
import rpy2.robjects as r
from main import load_dataset, install_packages

def plot(path,model):
    r.r(f'''
        png("{path}/img/{model}.png", width=800, height=600)
        plot({model}, label=FALSE)
        dev.off() 
    ''')

def plot_cv_mse_vs_lambda(path,model,alpha):
    r.r(f'''
    png("{path}/img/cv_mse_vs_lambda.png", width=800, height=600)
    plot({model}, xvar="lambda", label=TRUE,
            main = "CV–MSE vs log(lambda) per Elastic Net (α = {alpha})")
    dev.off()
    ''')

def plot_cv_mse_vs_alpha(path):
    r.r(f'''
    library(ggplot2)
    png("{path}/img/cv_mse_vs_alpha.png", width=800, height=600)
    p <- ggplot(results, aes(x = alpha, y = cvm_min)) +
        geom_line(color = "blue") +
        geom_point(color = "red") +
        xlab(expression(alpha)) +
        ylab("CV–MSE minimo") +
        ggtitle("Errore di cross–validation minimo in funzione di alpha") +
        theme_minimal()
    print(p)
    dev.off()
    ''')

if __name__ == "__main__":
    load_dotenv()
    PATH = os.getenv("DATASET_PATH")
    DATASET_NAME = os.getenv("DATASET_NAME")

    install_packages(["glmnet","ggplot2"])
    
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

    lambda_grid = r.r("""lambda_grid <- 10^seq(10, -10, length = 200)
                      lambda_grid""")

    print("Lambda Grid:\n",lambda_grid)

    lambda_best = r.r(f'''
        library(glmnet)
        set.seed(123)
        X_matrix <- as.matrix(ds[ , !(names(ds) %in% c("Crime")) ])
        y_vector <- as.vector(ds$Crime)
        ridge_model <- cv.glmnet(X_matrix, y_vector,alpha=0, nfolds = 5, lambda = lambda_grid)       
        best_lambda <- ridge_model$lambda.min
        best_lambda
    ''')

    plot(PATH,"ridge_model")

    best_ridge = r.r(f'''
        best_ridge <- glmnet(X_matrix, y_vector,lambda=best_lambda, nfolds = 5,alpha=0)
        lse <- best_ridge$lambda.1se
        best_ridge
    ''')

    best_aplha = r.r(f''' 
        alpha_grid <- seq(0, 1, by = 0.01)
        set.seed(123)
        results <- data.frame(
            alpha      = numeric(),
            lambda_min = numeric(),
            lambda_1se = numeric(),
            cvm_min    = numeric()
        )

        cv_models <- list()
                      
        for (a in alpha_grid) {{
            cv_fit <- cv.glmnet(X_matrix, y_vector, alpha = a, nfolds = 5, lambda = lambda_grid)
            best_index <- which.min(cv_fit$cvm)
            results <- rbind(
                results,
                data.frame(
                    alpha      = a,
                    lambda_min = cv_fit$lambda.min,
                    lambda_1se = cv_fit$lambda.1se,
                    cvm_min    = cv_fit$cvm[best_index]
                )
            )
            cv_models[[as.character(a)]] <- cv_fit
        }}
                      
        results[which.min(results$cvm_min), ]
    ''')

    en_estimator = r.r(f'''
        best_alpha <- {best_aplha.rx2('alpha')[0]}
        best_lambda <- {best_aplha.rx2('lambda_min')[0]}
        lambda_1se <- {best_aplha.rx2("lambda_1se")[0]}
        cv_en_model <- cv.glmnet(X_matrix,y_vector, alpha = best_alpha, lamdba = lambda_grid, standardize = TRUE)
        en_model <- glmnet(X_matrix, y_vector, alpha = best_alpha, lambda = best_lambda)
        en_model
    ''')

    plot_cv_mse_vs_lambda(PATH,"cv_en_model",best_aplha.rx2('alpha')[0])
    plot_cv_mse_vs_alpha(PATH)

    print(f"Ridge Regression - Optimal Lambda: {best_aplha.rx2('lambda_min')[0]}")
    print("Ridge Regression Coefficients:\n", r.r('coef(best_ridge)'))
    print("Results Alpha Elastic Net:\n", r.r("results"))
    print("Alpha Elastic Net Results:\n", best_aplha.rx2('alpha')[0])
    print("Elastic Net Coefficients:\n", r.r('coef(en_model)'))
