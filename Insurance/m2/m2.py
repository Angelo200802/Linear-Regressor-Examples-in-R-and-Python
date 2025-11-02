import rpy2.robjects as ro

#Read data from a CSV file using R
data = ro.r('read.csv("/home/angelo/Project/uni/MS_SL/ms_sl_ws/Insurance/insurance.csv",header=TRUE)')

#Select variables BMI and charges
x1 = data.rx2('bmi')
x2 = data.rx2('age')
x3 = data.rx2('children')
y = data.rx2('charges')

ro.globalenv['data'] = data
ro.globalenv['x1'] = x1
ro.globalenv['x2'] = x2
ro.globalenv['x3'] = x3
ro.globalenv['y'] = y

W = ro.r('W <- cbind(y,x1,x2,x3)')
print("### Statistical Summary of Variables")
print(ro.r('summary(W)'))

print("### Variance of Variables")
print(ro.r('var(W)'))    

print("### Correlation index between Variables")
print(ro.r('cor(W)'))

ro.r('''
    png("m2_dispersion.png", width=800, height=600)
    pairs(data[,c(1,3,4,7)])
    title("Disperion Matrix: Charges vs BMI vs Age vs Children")
    dev.off()
     ''')


model2 = ro.r('lm(y ~ x1+x2+x3)')
ro.globalenv['model2'] = model2
print("### Summary of Linear Model M2")
print(ro.r('summary(model2)'))

#Confronto tra ordinate stimate e osservate
ro.r('''
    png("m2_sy_vs_y.png", width=800, height=600)
    sy <- fitted(model2)
    plot(sy,y, xlab="Fitted Values", ylab="Observed Values", main="Fitted vs Observed Values for Model M2")
    abline(0,1,col="red")
    dev.off()
    ''')