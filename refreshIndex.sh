#!/bin/bash

if [ ! -f Scrapy/metadata.dat ]; then
    echo "Scapy/metadata.dat not found. Run scrapeAll.sh first"
    exit
fi

if [ ! "$(ls -A Scrapy/documents)" ]; then 
	echo "Scrapy/documents has no files. Run scrapeAll.sh first";
	exit
fi

rm -rfd Meta/PodcastDataSet/documents
cp -TR Scrapy/documents Meta/PodcastDataSet/documents
cp Scrapy/metadata.dat  Meta/PodcastDataSet/metadata.dat
cd Meta/PodcastDataSet
ls -1 documents/* | awk '$0="[none] "$0' > dataset-full-corpus.txt 
cd ..
rm -rfd idx*
python refreshIndex.py
cd ..