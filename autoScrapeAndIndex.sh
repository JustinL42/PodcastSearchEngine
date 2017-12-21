#!/bin/bash
echo "* Starting autoScrapeAndIndex.sh"

./scrapeAll.sh
./refreshIndex.sh
./generateAtypicalTerms.sh
