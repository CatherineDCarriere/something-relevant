install.packages('caret')
install.packages('ROCR')
install.packages('e1071') 

library('caret')
library('ROCR')
library('e1071')

tweetData <- read.csv("features.csv")

formula_text <- paste(names(tweetData[9]), "~", paste(names(tweetData[1:8]), collapse = "+"))
formula <- as.formula(formula_text)
#random 70% training vs. 30% testing
#rn_train <- sample(nrow(tweetData), floor(nrow(tweetData)*.7))
#train <- tweetData[rn_train,]
#test <- tweetData[-rn_train,]

fit <- lm(formula1, data = train)
test$scores <- predict(fit, type = "response", newdata = test)
pred<-prediction(test$scores, test1$F7_is_relevant)

#view results
head(test)
pred

#Confusion Matrix
confusion <- confusionMatrix(as.integer(test1$scores > 0.5), test1$F7_is_relevant)
confusion$table

#Standard ROC curve, true positive rate vs. false positive rate
perf <- performance(pred, 'tpr,' 'fpr')
plot(perf, lty = 1)