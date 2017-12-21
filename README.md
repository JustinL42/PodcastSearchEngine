# PodcastSearchEngine

A seach engine web app for scraping, indexing and searching podcast transcripts.

Requirements:

The install instructions have been tested on a new installation of Ubuntu Linux version 16.04 LTS but will likely work with only minor changes on other OS's as well. The web app can be run on any system with python installed, including Windows. The scripts to re-scrape the podcast transcipts and to rebuild the indexes and metadata require bash.

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



