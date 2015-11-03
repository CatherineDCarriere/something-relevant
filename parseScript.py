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
		if line["shared_parent_id"] != "":
			thisLine = {"F2_is_retweet": 1}
			outputList.append(thisLine)
		else:
			thisLine = {"F2_is_retweet": 0}
			outputList.append(thisLine)
	zippedLists = map(merge_two_dicts, outputList, dictList)
	return zippedLists

def fromDictListToCSV(dictList):
	headers = dictList[0].keys() #["id_str", "F1_has_punct", "F2_is_retweet"]
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
# output to features table as CSV
fromDictListToCSV(retweetList)

#dictKeys = ["feed_id", "id_str", "origin_id_str", "author_id", "replied_parent_id","shared_parent_id","message",
#	"story","sentiment","intent","posted_at","day","day_of_year","day_of_week","hour_of_day","replied_parent_origin_id_str",
#	"origin_url","created_at","updated_at","words","sentiment_score","network","old_type"]


