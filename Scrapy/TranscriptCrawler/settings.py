BOT_NAME = 'TranscriptCrawler'

SPIDER_MODULES = ['TranscriptCrawler.spiders']
NEWSPIDER_MODULE = 'TranscriptCrawler.spiders'

CONCURRENT_REQUESTS=32
DOWNLOAD_DELAY=2
CONCURRENT_REQUESTS_PER_DOMAIN=8

ITEM_PIPELINES = {
   'TranscriptCrawler.pipelines.TranscriptPipeline': 500,
}

AUTOTHROTTLE_ENABLED=True
AUTOTHROTTLE_START_DELAY=5
AUTOTHROTTLE_MAX_DELAY=60

HTTPCACHE_ENABLED=True

#to fix "Caught exception reading instance data" error.
DOWNLOAD_HANDLERS={'s3': None}
