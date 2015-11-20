# -*- coding: utf-8 -*-
import sys
import csv
import re

fileName = sys.argv[1]
# fileName = "HotelMsg123.csv"
content = []
with open(fileName) as f:
	content = list(csv.DictReader(f))

def merge_two_dicts(x, y):
    # Given two dicts, merge them into a new dict as a shallow copy.
    z = x.copy()
    z.update(y)
    return z

def getIdStrTable(sourceTable):
	outputList = []
	for dictionary in sourceTable:
		outputList.append({"id_str": dictionary['id_str']})
	return outputList

def findpunct(sourceTable, dictList):
	outputList = []
	for line in sourceTable:
		match = re.search("(!|\?)", line["message"])
		if match:
			thisLine = {"F1_has_punct": 1}
			outputList.append(thisLine)
		else:
			thisLine = {"F1_has_punct": 0}
			outputList.append(thisLine)
	zippedLists = map(merge_two_dicts, outputList, dictList)
	return zippedLists

def findRetweets(sourceTable, dictList):
	outputList = []
	for line in sourceTable:
		if line["rtcount"]:
			thisLine = {"F2_retweet_count": line["rtcount"]}
			outputList.append(thisLine)
		else:
			thisLine = {"F2_retweet_count": 0}
			outputList.append(thisLine)
	zippedLists = map(merge_two_dicts, outputList, dictList)
	return zippedLists

def countMatches(sourceTable, dictList, regex, outputColumnName):
	outputList = []
	for line in sourceTable:
		match = re.findall(regex, line["message"])
		thisLine = {outputColumnName: len(match)}
		outputList.append(thisLine)

	zippedLists = map(merge_two_dicts, outputList, dictList)
	return zippedLists

def markEnglish(sourceTable, dictList):
	outputList = []
	for line in sourceTable:
		thisLine = {'F6_is_english': line["english"]}
		outputList.append(thisLine)
	zippedLists = map(merge_two_dicts, outputList, dictList)
	return zippedLists

def markRelevant(sourceTable, dictList):
	outputList = []
	for line in sourceTable:
		thisLine = {'F7_is_relevant': line["relevance"]}
		outputList.append(thisLine)
	zippedLists = map(merge_two_dicts, outputList, dictList)
	return zippedLists

def markFeed(sourceTable, feedList, outputString):
	outputList = []
	for line in sourceTable:
		if int(line["feed_id"]) in feedList:
			thisLine = {outputString: 1}
			outputList.append(thisLine)
		else:
			thisLine = {outputString: 0}
			outputList.append(thisLine)
	return outputList

def markKeyword(sourceTable):
	return markFeed(sourceTable, [123, 124, 125, 128, 222, 225], "F8_is_keyword_feed")
	

def markHashtag(sourceTable):
	return markFeed(sourceTable, [174, 187, 188, 195, 220, 226], "F9_is_hashtag_feed")

def markDM(sourceTable):
	return markFeed(sourceTable, [127, 144, 186, 223, 224, 228], "F10_is_DM_feed")

def mergeFeedLists(sourceTable, dictList):
	keywordMerge = map(merge_two_dicts, markKeyword(content), dictList)
	hashtagMerge = map(merge_two_dicts, markHashtag(content), keywordMerge)
	dmMerge = map(merge_two_dicts, markDM(content), hashtagMerge)
	return dmMerge

def tweetLength(sourceTable, dictList):
	outputList = []
	for line in sourceTable:
		thisLine = {"F11_tweet_length": len(line["message"])}
		outputList.append(thisLine)
	zippedLists = map(merge_two_dicts, outputList, dictList)
	return zippedLists	

def fromDictListToCSV(dictList):
	headers = sorted(dictList[0].keys()) #["id_str", "F1_has_punct", "F2_is_retweet"]
	output = []
	#for memberDict in dictList:
	#	output.append(memberDict.values())
	with open("features.csv", "wb") as myfile:
		wr = csv.DictWriter(myfile, quoting = csv.QUOTE_MINIMAL, fieldnames = headers)
		wr.writeheader()
		wr.writerows(dictList)


# Create list of dicts with only "id_str" key
idTable = getIdStrTable(content)
# Merge in F1 - has ! or ? in message
punctList = findpunct(content, idTable)
# Merge in F2 - is a retweet?
retweetList = findRetweets(content, punctList)
# Merge in F3 - count of !
countBangList = countMatches(content, retweetList, "!", "F3_!_count")
# Merge in F4 - count of ?
countInterroList = countMatches(content, countBangList, "\?", "F4_?_count")
# Merge in F5 - count of hyperlinks
countLinkList = countMatches(content, countInterroList, "https?://", "F5_link_count")
# Merge in F6 - is English?
englishList = markEnglish(content, countLinkList)
# Merge in F7 - is relevant?
relevantList = markRelevant(content, englishList)
# Merge in F8, F9, F10 - feed type
keywordList = mergeFeedLists(content, relevantList)
# Merge in F11 - tweet length
tweetLengthList = tweetLength(content, keywordList)
# Merge in F12 - number of digits
countDigitsList = countMatches(content, tweetLengthList, "\d", "F12_digit_count")
# Merge in F13 - number of alphabet characters
countCharactersList = countMatches(content, countDigitsList, re.compile("[^\W\d\s_]", re.UNICODE), "F13_character_count")
# Merge in F14 - number of @ mentions
countMentionsList = countMatches(content, countCharactersList, "@[A-Za-z0-9_-]*", "F14_mentions_count")
# Merge in F15 - number of money expressions
countMoneyList = countMatches(content, countMentionsList, "[\$|€|¥|£|₨]\d+(?:(?:,|\.)\d{2}|\b)", "F15_money_expressions_count")
# Merge in F16 - number of hashtags
countHashtagList = countMatches(content, countMoneyList, "#[A-Za-z0-9_-]*", "F16_hashtag_count")
# Merge in F17 - number of " - "
countDashList = countMatches(content, countHashtagList, " - ", "F17_dash_count")
# Merge in F18 - number of "words"
countWordsList = countMatches(content, countDashList, re.compile("[^\W\d\s_]+", re.UNICODE), "F18_word_count")

# output to features table as CSV
fromDictListToCSV(countWordsList)

#dictKeys = ["feed_id", "id_str", "origin_id_str", "author_id", "replied_parent_id","shared_parent_id","message",
#	"story","sentiment","intent","posted_at","day","day_of_year","day_of_week","hour_of_day","replied_parent_origin_id_str",
#	"origin_url","created_at","updated_at","words","sentiment_score","network","old_type"]


