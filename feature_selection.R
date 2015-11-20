#Feature Selection Script - Create your desired formulas
#RUN AFTER Tweet_Env_Setup.R

#pick out 14 features from data, exclude class (F07) 
features <- names(tweetData[c(1:6,8,11,12,14:18)])

#formList: function to create exhaustive list of formulas using n features
#NOTE: MAY BE COMPUTATIONALLY EXPENSIVE AT HIGH N
formList <- function(dat, features, n) {
  formulaList <- list()
  combinations <- combn(features,n)
  for (k in 1:ncol(combinations)) {
    formula_text_comb <- paste(names(dat[7]), "~", paste(combinations[,k], collapse = "+"))
    formula_comb <- as.formula(formula_text_comb)
    formulaList[k] <- list(formula_comb)
  }
  return(formulaList)
}

#choose how many features you want in your optimal feature set
#EXAMPLES:
formulaList3 <- formList(tweetData, features, 3)
formulaList5 <- formList(tweetData, features, 5)
formulaList7 <- formList(tweetData, features, 7)

#using predictionList from Tweet_Env_Setup.R, test formulas using AUC scores
#AUC scores are averaged across folds and compared pair-wise between feature sets
AUCtester <- function(dat, formulas) {
  #extract formulas, then run analysis
  form1 <- formulas[[1]]
  for (k in 2:length(formulas)){
    form2 <- formulas[[k]] 
    comboPred1 <- predictionList(dat, form1)[[4]]
    AUCperf1 <- performance(comboPred1, 'auc')
    #average AUCperf1@y.values
    AUC1avg <- mean(c(AUCperf1@y.values[[1]], AUCperf1@y.values[[2]], AUCperf1@y.values[[3]], AUCperf1@y.values[[4]]))
    comboPred2<- predictionList(dat, form2)[[4]]
    AUCperf2 <- performance(comboPred2, 'auc')
    #average AUCperf2@y.values
    AUC2avg <- mean(c(AUCperf2@y.values[[1]], AUCperf2@y.values[[2]], AUCperf2@y.values[[3]], AUCperf2@y.values[[4]]))
    #winner <- larger average AUC
    if (AUC1avg > AUC2avg) {
      form1 <- form1
    } else {
      form1 <- form2
    }
  }
  return(form1)
}

#Example command to get the best 3 features. Output is data type:formula
#NOTE: MAY BE COMPUTATIONALLY EXPENSIVE AT HIGH NUMBERS OF FEATURES
best3Features <- AUCtester(tweetData, formulaList3)

#To add features ad hoc to existing formulas, use, for example:
best3Plus1 <- update(best3Features, .~. + F11_tweet_length)

#Now you are ready to plot the performance of your features using 
#Feature_Set_Comparison_Script.
