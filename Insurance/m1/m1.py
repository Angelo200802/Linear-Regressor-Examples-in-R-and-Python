import rpy2.robjects as ro

print(ro.r('R.version.string'))

#Read data from a CSV file using R
data = ro.r('read.csv("/home/angelo/Project/uni/MS_SL/ms_sl_ws/Insurance/insurance.csv",header=TRUE)')

#Select variables BMI and charges
x1 = data.rx2('bmi')
y = data.rx2('charges')

ro.globalenv['data'] = data
ro.globalenv['x1'] = x1
ro.globalenv['y'] = y

W = ro.r('W <- cbind(y,x1)')
ro.r('''
     png("hist_charges.png", width=800, height=600)
     hist(y)
     dev.off()''')

print("### Statistical Summary of Variables")
print(ro.r('summary(W)'))

print("### Variance of Variables")
print(ro.r('var(W)'))    

print("### Correlation index between Variables")
print(ro.r('cor(W)'))

ro.r('''
    png("m1_scatter_plot.png", width=800, height=600)
    plot(data[,c(3,7)])
    abline(lm(y ~ x1), col="red")
    title("Regression Line: Charges vs BMI")
    dev.off()
     ''')

model1 = ro.r('lm(y ~ x1)')
ro.globalenv['model1'] = model1
print("### Summary of Linear Model M1")
print(ro.r('summary(model1)'))

## Residuals Analysis
ro.r('''
     png("m1_residuals.png", width=800, height=600)
     hist(resid(model1), main="Histogram of Residuals for Model M1", xlab="Residuals")
     dev.off()''')