import os, re, unicodecsv
scrapyDir = os.path.dirname(os.path.dirname(__file__))
documentsDir = os.path.join(scrapyDir, "documents")

class TranscriptPipeline(object):

	def remove_non_ascii(self, text):
		return ''.join(i for i in text if ord(i)<128)

	def process_item(self, item, spider):
		if item.get('transcript', '') == '':
			print("transcript missing for " +
				  item.get('podcast_name', "unknown podcast"))
			return item



		if not os.path.exists(documentsDir):
			os.makedirs(documentsDir)

		if (len(os.listdir(documentsDir)) == 0):
			next_doc = 0
		else:
			last_doc = sorted(os.listdir(documentsDir))[-1]
			next_doc = 1 + int(re.match("doc(\d\d\d\d\d).txt", last_doc).group(1))

		item['docID'] = next_doc
		filename = "doc" + '%05d' % next_doc + ".txt"
		writer = unicodecsv.writer(open(os.path.join(documentsDir, filename), 'wb'), 
								   delimiter="\t", lineterminator='\n')
		writer.writerow([item['transcript']])

		writer = unicodecsv.writer(open(os.path.join(scrapyDir, "metadata.dat"), 'ab'), 
			                	   delimiter="\t", lineterminator='\n')
		item['date_published'] = self.remove_non_ascii(item.get('date_published', "")) 
		writer.writerow([item.get(key, " ") for key in ['docID', 'podcast_name', 'episode_title', 
											   'subsection', 'date_published', 'transcript_url', 
											   'listen_url', 'atypical_terms']])
		return item