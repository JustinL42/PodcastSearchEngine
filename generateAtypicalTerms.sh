#!/bin/bash

collection[0]="Freakonomics"
collection[1]="Wait Wait... Don't Tell Me!"
collection[2]="Ted Radio Hour"
collection[3]="Invisibilia"
collection[4]="All Things Considered"

cd Meta
for ((i=0;i<${#collection[*]};i++)); do
	#create a config file for each podcast's collection
    cp config.toml config$i.toml
    find config$i.toml -type f -exec sed -i "s/file/file$i/g" {} \;
    find config$i.toml -type f -exec sed -i "s/idx/idx$i/g" {} \;

	#create a file corpus config file for each podcast's collection
    cp PodcastDataSet/file.toml PodcastDataSet/file$i.toml
    find PodcastDataSet/file$i.toml -type f -exec sed -i "s/dataset/dataset$i/g" {} \;

    #generate the full corpus file list for each collection
	grep -Prho "^(\d+)\t${collection[i]}" PodcastDataSet/metadata.dat | cut -f1 | awk '{printf("%05d\n", $1)}' | awk '{print "[none] documents/doc"$0".txt"}' > PodcastDataSet/dataset$i-full-corpus.txt

	#generate indexes for each collection
	python refreshIndex.py $i

done
cd ..

python generateAtypicalTerms.py

cp Meta/PodcastDataSet/atypicalTerms.txt  Meta/PodcastDataSet/metadata.dat
rm Meta/PodcastDataSet/atypicalTerms.txt
rm -rfd Meta/idx

cd Meta
python refreshIndex.py
cd ..

