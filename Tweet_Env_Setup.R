#Twitter Data Analysis Environment Setup Script - RUN FIRST

#install and load libraries
install.packages('caret')
install.packages('ROCR')
install.packages('e1071')
install.packages('rpart')

library('caret')
library('ROCR')
library('e1071')
library('rpart')

#import data
#navigate to the directory in which you downloaded your data.
#Note that at present, this script works only with data containing
#400 rows and having at least 17 *correctly ordered* columns
#This is ensured by using the parseScript.py on your scored data
setwd("~/yourpath/directorywithdata")
tweetData <- read.csv("400_records_18_features.csv")

#now define functions for analysis using n-fold cross-validation

#predictionList: function to create models and predictions
#using user-defined data and formula
predictionList <- function(dat, form, n){
  predList <- list()
  fitList <- list()
  testsetList <- list()
  f <- gl(n, floor(nrow(dat)/n), length = nrow(dat))
  dat$folds <- f
  scoresMatrix <- matrix(nrow=floor(nrow(dat)/n), ncol=n, byrow = FALSE)
  actualMatrix <- matrix(nrow=floor(nrow(dat)/n), ncol=n, byrow = FALSE)
  for (k in 1:n) {
    train <- dat[(dat$folds != k),]
    train <- train[1:floor(nrow(dat)/n),]
    test <- dat[(dat$folds == k),]
    test <- test[1:floor(nrow(dat)/n),]
    fit <- lm(form, data = train)
    test$scores <- predict(fit, type = "response", newdata = test)
    scoresMatrix[,k] <- test$scores
    actualMatrix[,k] <- test$F07_is_relevant
    comboPred <- prediction(scoresMatrix, actualMatrix)
    pred <- prediction(test$scores, test$F07_is_relevant)
    predList[k] <- pred
    fitList[k] <- list(fit)
    testsetList[k] <- list(test)
  }
  bigList <- list(predList,list(fitList),list(testsetList),comboPred)
  return(bigList)
  #return(bigList)
}

#getConfusions: function to get all the confusion tables 
#for cross-validation runs at a specified threshold 
getConfusions <- function(testers, threshold) {
  confList <- list()
  for (k in 1:4) {
    conf <- confusionMatrix(as.integer(testers[[k]]$scores > threshold), 
                            testers[[k]]$F07_is_relevant, positive = '1')
    confList[k] <- list(conf)
  }
  return(confList)
}

#getROCs: function to construct ROC curves using predictions 
#(formal class 'predictions')
getROCs <- function(preds) {
  ROCList <- list()
  for (k in 1:4) {
    perf <- performance(preds[[k]], 'tpr', 'fpr')
    ROCList[k] <- perf
  }
  return(ROCList)
}

#ROCPlot: function to plot all ROCs on one graph
ROCPlot <- function(ROCs, ttl) {
  plot(ROCs[[1]], lty = 1, col = "blue", main = ttl)
  plot(ROCs[[2]], lty = 1, col = "green", add = TRUE)
  plot(ROCs[[3]], lty = 1, col = "purple", add = TRUE)
  plot(ROCs[[4]], lty = 1, col = "cyan", add = TRUE)
  abline(0, 1, lty = 1, col = "red")
  legend(0.6,0.3, c("Trial 1", "Trial 2", "Trial 3", "Trial 4", "Average"), 
         lty = c(1,1,1,1), col=c("blue","green", "purple", "cyan", "black"))
  avgperf <- performance(comboPred, 'tpr', 'fpr')
  plot(avgperf, lty = 1, avg = "threshold", add = TRUE)
}


