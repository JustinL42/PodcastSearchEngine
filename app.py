import metapy, os, re
from flask import Flask, request, render_template
app = Flask(__name__)
MetaDir = os.path.join(os.path.dirname(__file__), "Meta")

def underlineST(prop, searchTerm):
	tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
	tok.set_content(searchTerm)
	uniqueTerms = set(x for x in tok)
	for term in uniqueTerms:
		prop = re.sub("(" + term + ")", r"<u>\1</u>", 
					  prop, flags=re.IGNORECASE)
	return prop

def exists(prop):
	return prop and prop.strip() != '' and prop != None and \
	prop.lower() != "none" and prop.lower() != "null"

@app.route('/')
def search():
	resultHTML = []
	searchTerm = request.args.get('searchTerm', '')
	if searchTerm:
		# invert index needs to be called in the config's folder
		os.chdir(MetaDir)
		idx = metapy.index.make_inverted_index('config.toml')
		ranker = metapy.index.OkapiBM25()
		query = metapy.index.Document()
		query.content(searchTerm)
		top_docs = ranker.score(idx, query, num_results=10)

		for doc in top_docs:
			md = idx.metadata(doc[0])
			result = []
			result.append("<p>Podcast: <b>" + md.get('podcast name') + "</b></p>\n")

			episode = md.get('episode name')
			if exists(episode):
				result.append("<p>Episode: <b>" + underlineST(episode, searchTerm) + "</b></p>\n")

			subsection = md.get('subsection')
			if exists(subsection):
				result.append("<p>Subsection: <b>" + underlineST(subsection, searchTerm) + "</b></p>\n")

			result.append("<p>Score: " + str(doc[1]) )

			date = md.get('date published')
			if exists(date):
				result.append("\t|\tDate published: " + date + "</p>\n")
			else: 
				result.append("</p>\n")

			atypicalTerms = md.get('atypical terms')
			if exists(atypicalTerms):
				result.append("<p>Atypical terms: " + underlineST(atypicalTerms, searchTerm) + "</p>\n")

			result.append("<p><a href=\"" + md.get('transcript url') + 
				"\">Read transcript</a> | <a href=\"" + md.get('listen url')  +
				"\">Listen to episode</a></p>")

			resultHTML.append(result)

	return render_template('page.html', searchTerm=searchTerm, resultHTML=resultHTML)