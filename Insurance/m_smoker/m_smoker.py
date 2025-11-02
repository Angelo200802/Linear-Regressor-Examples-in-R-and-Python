import rpy2.robjects as ro

dataset = ro.r('read.csv("/home/angelo/Project/uni/MS_SL/ms_sl_ws/Insurance/insurance.csv",header=TRUE)')

ro.globalenv['ds'] = dataset

# Sostituisco la variabile categorica smoker con una variabile numerica binaria
ro.r('''
     ds$smoker <- ifelse(ds$smoker == "yes", 1, 0)
     ''')



x = ro.globalenv['ds'].rx2('smoker')
y = dataset.rx2('charges')

ro.globalenv['x'] = x
ro.globalenv['y'] = y

ro.r('''
    png("ms_scatter_plot.png", width=800, height=600)
    plot(ds[,c(5,7)])
    abline(lm(y ~ x), col="red")
    title("Regression Line: Charges vs Smokers")
    dev.off()
     ''')

model = ro.r('lm(y ~ x)')
ro.globalenv['m'] = model
print("### Summary of Linear Model with only Smoker as Predictor")
print(ro.r('summary(m)'))


#Aggiungiamo le variabili bmi e age al modello
x1 = dataset.rx2('bmi')
ro.globalenv['x1'] = x1
x2 = dataset.rx2('age')
ro.globalenv['x2'] = x2

model_smoker = ro.r('lm(y ~ x + x1 + x2)')
ro.globalenv['m1'] = model_smoker
print("### Summary of Linear Model with Smoker, Age and BMI as Predictor")
print(ro.r('summary(m1)'))

#Aggiungiamo le variabili children al modello
x3 = dataset.rx2('children')
ro.globalenv['x3'] = x3

W = ro.r('W <- cbind(y,x,x1,x2,x3)')
print("### Statistical Summary of Variables")
print(ro.r('summary(W)'))

print("### Correlation index between Variables")
print(ro.r('cor(W)'))

ro.r('''
    png("ms_dispersion.png", width=800, height=600)
    pairs(ds[,c(1,3,4,5,7)])
    title("Disperion Matrix: Charges vs BMI vs Age vs Children")
    dev.off()
     ''')

model_smoker2 = ro.r('lm(y ~ x + x1 + x2 + x3)')
ro.globalenv['m2'] = model_smoker2
print("### Summary of Linear Model with Smoker, BMI, Age and Children as Predictors")
print(ro.r('summary(m2)'))