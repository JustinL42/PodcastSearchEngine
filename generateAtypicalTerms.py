import metapy, os, unicodecsv, codecs
MetaDir = os.path.join(os.path.dirname(__file__), "Meta")
DataSetDir = os.path.join(MetaDir, "PodcastDataSet")


podcastNumber = {"Freakonomics" : "0",
"Wait Wait... Don't Tell Me!": "1",
"Ted Radio Hour": "2",
"Invisibilia": "3",
"All Things Considered": "4",
"test" : "5"}

def getaTermString(docString, podcastName):

	num = podcastNumber.get(podcastName, "")
	if not(num):
		print(podcastName + " not in list error")
		return " "

	os.chdir(MetaDir)
	idx = metapy.index.make_inverted_index("config" + num + ".toml")
	os.chdir("..")

	doc = metapy.index.Document()
	doc.content(docString)

	tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
	tok = metapy.analyzers.LowercaseFilter(tok)
	tok = metapy.analyzers.ListFilter(tok, "Meta/metaSupportFiles/stopwords.txt", 
										metapy.analyzers.ListFilter.Type.Reject)
	tok = metapy.analyzers.LengthFilter(tok, min=2, max=30)
	ana = metapy.analyzers.NGramWordAnalyzer(1, tok)
	thisDocsTermFreq = ana.analyze(doc)

	aTermTuples = []

	for word, freq in thisDocsTermFreq.items():

		indexTermID = idx.get_term_id(word)
		if not(idx.term_text(indexTermID)):
			continue

		typicallityRatio = float(idx.total_num_occurences(indexTermID)) / freq
		aTermTuples.append((typicallityRatio, word))

	maxTerms = min(15, len(aTermTuples))
	sortedList = sorted(aTermTuples, key=lambda tup: (tup[0], -len(tup[1])))
	aTermList = [ tup[1] for tup in sortedList[0:maxTerms]]
	return ", ".join(aTermList)


aTermFile = os.path.join(DataSetDir, "atypicalTerms.txt")

try:
	os.remove(aTermFile)
except:
	pass

reader = unicodecsv.reader(open(os.path.join(DataSetDir, "metadata.dat"), 'rb'), 
			                	   delimiter="\t", lineterminator='\n')

writer = unicodecsv.writer(open(aTermFile, 'ab'), 
	                	   delimiter="\t", lineterminator='\n')

for row in reader:
	try:
		docID = row[0]
		podcastName = row[1]
		docName = "doc" + '%05d' % int(docID) + ".txt"

		with codecs.open(os.path.join(DataSetDir, "documents", docName), 'rb', encoding='utf-8') as docFile:
			docString = docFile.read()

		docATerms = getaTermString(docString, podcastName)
		writer.writerow(row[0:-1] + [docATerms])
	except:
		writer.writerow(row [0:-1] + [" "])


