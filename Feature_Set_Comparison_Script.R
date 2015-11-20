#Results Comparison Script

#first load libraries, data, and functions using Tweet_Env_Setup.R

#Then load feature_selection.R and create desired formulas

#then set formula and title of plot
#formula <- whateverFormula #formula type
#plotTitle <- "whateverTitle"

#------------------------then run:------------------------# 

#extract predictions from cross-validation runs
predictions <- predictionList(tweetData, formula)[[1]]

#extract models using predictionList
getfits <- predictionList(tweetData, formula)[[2]]
fits <- getfits[[1]]

#extract test sets using predictionList
gettestsets <- predictionList(tweetData, formula)[[3]]
testsets <- gettestsets[[1]]

#extract predictions as a matrix for average performance plot
comboPred <- predictionList(tweetData, formula)[[4]]

#get list of ROCs (formal class 'performance') using predictions
ROCs <- getROCs(predictions)

#draw plot
ROCPlot(ROCs, plotTitle)

#get AUC, cross-validation runs 
AUCperf <- performance(comboPred, 'auc')
AUCperf@y.values #compare AUC for all CV runs

#---------------------COMPARING RESULTS-------------#

#To add features ad hoc to existing formulas, simply add new features
#to whatever formulas you have in the environment.
#Try, for example:
formula <- update(formula, .~. + F11_tweet_length)

#---------------------OPTIONAL-------------------#

#You can run getConfusions to generate a list of confusion tables
#for each of your cross-validation runs. Just run the following, 
#setting your threshold as desired. For example:

#extract a confusion table at threshold 0.5
getconfs <- getConfusions(testsets, 0.5)
confusion1 <- getconfs[[1]]
confusion1
#or directly: confusion1 <- getConfusions(testsets, 0.5)[[1]]
