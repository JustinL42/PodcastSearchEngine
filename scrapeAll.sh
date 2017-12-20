#!/bin/bash
echo "* Starting scrapeAll.sh"

file="DO-NOT-SCRAPE.txt"
if [ -f "$file" ];
then
	echo "* $file found. This file is distributed with the code to prevent \
unintentinal scraping, which could overwhelm servers hosting \
transcripts if done repeatedly or incorrectly. If you are sure you want this \
application to scrape, delete or rename $file and re-run this script"

	exit
fi

echo "*$file not found. A scrape of podcast transcript websites will begin"
cd Scrapy
rm -rfd documents
rm -f metadata.dat
podcasts=( freakonomics waitwaitdonttellme tedradiohour invisibilia allthingsconsidered )
for podcast in "${podcasts[@]}"; do
	scrapy crawl $podcast --loglevel=ERROR
done
cd ..

