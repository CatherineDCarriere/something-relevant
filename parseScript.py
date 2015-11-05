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

def countBangs(sourceTable, dictList):
	outputList = []
	for line in sourceTable:
		match = re.findall("!", line["message"])
		thisLine = {"F3_!_count": len(match)}
		outputList.append(thisLine)

	zippedLists = map(merge_two_dicts, outputList, dictList)
	return zippedLists

def countInterro(sourceTable, dictList):
	outputList = []
	for line in sourceTable:
		match = re.findall("\?", line["message"])
		thisLine = {"F4_?_count": len(match)}
		outputList.append(thisLine)

	zippedLists = map(merge_two_dicts, outputList, dictList)
	return zippedLists

def countHttp(sourceTable, dictList):
	outputList = []
	for line in sourceTable:
		match = re.findall("https?://", line["message"])
		thisLine = {"F5_link_count": len(match)}
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

def markKeyword(sourceTable):
	outputList = []
	keyWordFeeds = [123, 124, 125, 128, 222, 225]
	for line in sourceTable:
		if int(line["feed_id"]) in keyWordFeeds:
			thisLine = {"F8_is_keyword_feed": 1}
			outputList.append(thisLine)
		else:
			thisLine = {"F8_is_keyword_feed": 0}
			outputList.append(thisLine)
	return outputList

def markHashtag(sourceTable):
	outputList = []
	keyWordFeeds = [174, 187, 188, 195, 220, 226]
	for line in sourceTable:
		if int(line["feed_id"]) in keyWordFeeds:
			thisLine = {"F9_is_hashtag_feed": 1}
			outputList.append(thisLine)
		else:
			thisLine = {"F9_is_hashtag_feed": 0}
			outputList.append(thisLine)
	return outputList

def markDM(sourceTable):
	outputList = []
	keyWordFeeds = [127, 144, 186, 223, 224, 228]
	for line in sourceTable:

		if int(line["feed_id"]) in keyWordFeeds:
			thisLine = {"F10_is_DM_feed": 1}
			outputList.append(thisLine)
		else:
			thisLine = {"F10_is_DM_feed": 0}
			outputList.append(thisLine)
	return outputList

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
countBangList = countBangs(content, retweetList)
# Merge in F4 - count of ?
countInterroList = countInterro(content, countBangList)
# Merge in F5 - count of hyperlinks
countLinkList = countHttp(content, countInterroList)
# Merge in F6 - is English?
englishList = markEnglish(content, countLinkList)
# Merge in F7 - is relevant?
relevantList = markRelevant(content, englishList)
# Merge in F8, F9, F10 - feed type
keywordList = mergeFeedLists(content, relevantList)
# Merge in F11 - tweet length
tweetLengthList = tweetLength(content, keywordList)
# output to features table as CSV
fromDictListToCSV(tweetLengthList)

#dictKeys = ["feed_id", "id_str", "origin_id_str", "author_id", "replied_parent_id","shared_parent_id","message",
#	"story","sentiment","intent","posted_at","day","day_of_year","day_of_week","hour_of_day","replied_parent_origin_id_str",
#	"origin_url","created_at","updated_at","words","sentiment_score","network","old_type"]


