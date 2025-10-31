import rpy2.robjects as ro

print(ro.r('R.version.string'))

#Read data from a CSV file using R
data = ro.r('read.csv("insurance.csv",header=TRUE)')

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
    dev.new()
    png("scatter_bmi_charges.png", width=800, height=600)
    plot(data[,c(3,7)],main="Scatter plot of BMI vs Charges")
    dev.off()
     ''')

model1 = ro.r('lm(y ~ x1)')
ro.globalenv['model1'] = model1
print("### Summary of Linear Model M1")
print(ro.r('summary(model1)'))