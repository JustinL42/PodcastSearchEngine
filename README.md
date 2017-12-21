# PodcastSearchEngine

A search engine web app for scraping, indexing and searching podcast transcripts.

Requirements:

The install instructions have been tested on a new installation of Ubuntu Linux version 16.04 LTS but will likely work with only minor changes on other OS's as well. The web app can be run on any system with python installed. The scripts to re-scrape the podcast transcripts and to rebuild the indexes and metadata require bash.

Installation:

Get pip and git if they aren't installed already:

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-pip git

Install the required python packages:

pip install metapy scrapy flask unicodecsv

Clone this git repository with:

git clone https://github.com/JustinL42/PodcastSearchEngine.git
cd PodcastSearchEngine

To run the app using the included index and metada:

./launchApp.sh

If the app doesn't automatically launch in your browser, manually open: 

http://127.0.0.1:5000/


To run the app without using the bash script:

python app.py

Architecture Overview:

The application is made of three parts: a web crawler built on Scrapy that gets the documents, indices made with Meta which analyze the documents and queries, and a simple web front end for running searches built with Flask. Scrapy stores the documents and metadata in the Scrapy folder, which are then copied to Meta folder for indexing and use by the front end. This repository doesn't actually contain the documents, only the indices and metadata from a previous crawl which can still be used to run the front end. 


Rebuilding the documents and indices:

The autoScrape.sh script can be called either manually or as scheduled task to periodically download new documents and rebuild the index and metada used by the search engine. It calls the following other scripts in sequence, which can also be called individually as needed: 

scrapeAll.sh
refreshIndex.sh
generateAtypicalTerms.sh


scrapeAll.sh: This runs all the spiders in the Scrapy project. See Scrapy/TranscriptCrawler/spiders.transcript_spider.py for details of this and Scrapy/TranscriptCrawler/pipelines.py for how the data is stored. This script won't run until the file DO-NOT-SCRAPE.txt is removed. This is to confirm the user knows the app will be scraping before it is done automatically by the script.

refreshIndex.sh: This deletes the old Meta document collection and metadata and copies the new data from the Scrapy project. The index is deleted and rebuild with the new data.

generateAtypicalTerms.sh: This is used to create the "atypical terms" list featured in the search results for each podcast episode or section. Terms are considered atypical if their occurrence in the document is high compared to their occurrence in the collection of documents for that podcast. These can help the user see which topics were discussed in that transcript. The script creates separate indices for each podcast, and the terms are then generated as metadata for each document.

To reset the index and metadata to its original state, use the git commands:

git fetch origin
git reset --hard origin/master


To add additional podcasts, build a new scrapy spider for it and add the podcasts name to the relevant scripts. Run autoScrape.sh and re-launch the app.