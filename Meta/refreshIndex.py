#!/usr/bin/python
import sys
import metapy

if len(sys.argv) >= 2:
	suffix = sys.argv[1]
else:
	suffix = ''
idx = metapy.index.make_inverted_index('config' + suffix + '.toml')
