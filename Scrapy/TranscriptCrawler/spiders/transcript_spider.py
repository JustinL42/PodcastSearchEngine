import scrapy
from scrapy.loader import ItemLoader
from TranscriptCrawler.items import PodcastTranscriptsItem

class NPRSpider(scrapy.Spider):
    max_iterations = 2
    nprPodcastName = "NPR"

    def parse(self, response):
        iteration = response.meta.get('iteration', 0)
        print(self.nprPodcastName + " page " + str(iteration))

        if iteration > self.max_iterations : 
            return

        episodes = response.css('article.program-show h2.program-show__title a::attr(href)')

        for episodeUrl in episodes.extract():
            request = scrapy.Request(
                episodeUrl, 
                callback=self.parseEpisode,
                dont_filter=True
            )
            yield request

        lastIDSelector = response.css('article.program-show').xpath('./@data-episode-id')
        lastDateSelector = response.css('article.program-show').xpath('./@data-episode-date')

        if (not(lastIDSelector) or not(lastDateSelector)):
            return

        lastID = lastIDSelector[-1].extract()
        lastDate = lastDateSelector[-1].extract()
        print("accessing " + self.nprPodcastName + " archive from date: " + lastDate)
        next_page = self.start_urls[0] + '?date=' + lastDate + '&eid=' + lastID
        yield scrapy.Request(
                            next_page, callback=self.parse, 
                            meta={'iteration': iteration + 1},
                            priority=0
        )


    def parseEpisode(self, response):
        print("parsing " + self.nprPodcastName + " episode")

        subsections = response.css('h3.rundown-segment__title a::attr(href)')
        for url in subsections.extract():
            l = ItemLoader(PodcastTranscriptsItem(), response)
            l.add_css('episode_title', 'div.title-description h1')
            request = scrapy.Request(
                url, 
                callback=self.parseSubsection,
                meta={'itemLoader': l},
                dont_filter=True,
                priority=75
            )
            yield request

    def parseSubsection(self, response):
        print("parsing " + self.nprPodcastName + " subsection")

        for linkToTranscript in response.css('li.audio-tool-transcript a::attr(href)').extract():
            request = scrapy.Request(
                linkToTranscript, 
                callback=self.parseTranscript,
                meta={'itemLoader': response.meta['itemLoader']},
                #dont_filter=True,
                priority=100
            )
            yield request
            break


    def parseTranscript(self,response):
        print("parsing " + self.nprPodcastName + " transcript")
        l = response.meta['itemLoader']
        l.selector = response

        l.add_css('subsection', 'div.storytitle h1 a::text')
        l.add_value('podcast_name', self.nprPodcastName)
        l.add_css('date_published', 'span.date')
        l.add_xpath('transcript', '//div[@class="transcript storytext"]//p[not(@class)]')
        l.add_value('transcript_url', response.url)
        l.add_value('listen_url', response.url)
        yield l.load_item()


class TedRadioHourSpider(NPRSpider):
    # max_iterations = 3
    name = "tedradiohour"
    nprPodcastName = "Ted Radio Hour"
    start_urls = ['https://www.npr.org/programs/ted-radio-hour/archive']

class AllThingsConsideredSpider(NPRSpider):
    max_iterations = 1
    name = "allthingsconsidered"
    nprPodcastName = "All Things Considered"
    start_urls = ['https://www.npr.org/programs/all-things-considered/archive']

class WWDTMTimeSpider(NPRSpider):
    # max_iterations = 3
    name = "waitwaitdonttellme"
    nprPodcastName = "Wait Wait... Don't Tell Me!"
    start_urls = ['http://www.npr.org/programs/wait-wait-dont-tell-me/archive']

class InvisibiliaSpider(NPRSpider):
    # max_iterations = 3
    name = "invisibilia"
    nprPodcastName = "Invisibilia"
    start_urls = ['https://www.npr.org/programs/invisibilia/archive']

    def parseTranscript(self,response):
        print("parsing " + self.nprPodcastName + " transcript")
        l = response.meta['itemLoader']
        l.selector = response

        #no subsection in this podcast
        l.add_value('podcast_name', self.nprPodcastName)
        l.add_css('date_published', 'span.date')
        l.add_xpath('transcript', '//div[@class="transcript storytext"]//p[not(@class)]')
        l.add_value('transcript_url', response.url)
        l.add_value('listen_url', response.url)
        yield l.load_item()


class FreakonomicsSpider(scrapy.Spider):
    name = "freakonomics"
    start_urls = ['http://freakonomics.com/tag/transcript/']
    allowed_domains = ['freakonomics.com']

    def parse(self, response):
        for link in response.css('div.article_content h2 a::attr(href)').extract():
            if link is not None:
                yield scrapy.Request(link, callback=self.parse_transcript)

        for  next_page in response.css('div.nav_next a::attr(href)').extract():
            if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parse)
                

    def parse_transcript(self, response):
        l = ItemLoader(item=PodcastTranscriptsItem(), response=response)
        l.add_css('episode_title',  'h1.single_title')
        l.add_css('date_published', 'div.article_meta time')
        l.add_css('transcript', 'article p')
        l.add_value('podcast_name', "Freakonomics")
        l.add_value('transcript_url', response.url)
        listen_url = l.get_xpath('//article[1]/p[1]//a[1]/@href')

        if listen_url:
            l.add_value('listen_url', listen_url)
        else:
            l.add_value('listen_url', response.url)

        return l.load_item() 