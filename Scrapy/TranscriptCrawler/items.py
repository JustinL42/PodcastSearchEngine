import scrapy
from scrapy.loader.processors import TakeFirst, Join, MapCompose
from w3lib.html import remove_tags


class PodcastTranscriptsItem(scrapy.Item):

    transcript = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )

    docID = scrapy.Field()

    podcast_name = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )

    episode_title = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )

    subsection = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )

    atypical_terms = scrapy.Field()

    date_published = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )

    transcript_url = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )

    listen_url = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    