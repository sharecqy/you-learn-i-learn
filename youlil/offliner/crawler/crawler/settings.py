# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#


SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'
USER_AGENT = '%s' % ('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)')
ITEM_PIPELINES = [
    'crawler.pipelines.GoogleNewsImagePipeline',
    'crawler.pipelines.StoreNewsIntoDbPipeline',
    'crawler.pipelines.PushUrlIntoQueuePipeline',
    
    'crawler.pipelines.NewsExtractPipeline',
    'crawler.pipelines.UpdateNewsInDbPipeline',
]

LOG_FILE='feed_spider.log'
LOG_LEVEL='INFO'
LOG_STDOUT=True
DOWNLOAD_TIMEOUT=50
ARTICLE_MIN_LENGTH=250
""" FeedSpider """
""" ArticleSpider """
"""
ITEM_PIPELINES = [
    
    'crawler.pipelines.DescriptionPipeline',
    'crawler.pipelines.FeedItemStorePipeline',
    
    
    'crawler.pipelines.ArticlePipeline',
    'crawler.pipelines.ArticleStorePipeline',
]
"""
eng_news={
          "world":["https://news.google.com/news/section?pz=1&cf=all&topic=w","https://news.google.com.hk/news/feeds?region=uk&pz=1&cf=all&ned=us&hl=en&topic=w&output=rss","https://news.google.com/news/feeds?region=au&pz=1&cf=all&ned=us&hl=en&topic=w&output=rss"],
          "technology":["https://news.google.com/news/feeds?pz=1&cf=all&ned=us&hl=en&topic=tc&output=rss","https://news.google.com.hk/news/feeds?region=uk&pz=1&cf=all&ned=us&hl=en&topic=tc&output=rss","https://news.google.com/news/feeds?region=au&pz=1&cf=all&ned=us&hl=en&topic=tc&output=rss"],
          "bussiness":["https://news.google.com/news/feeds?pz=1&cf=all&ned=us&hl=en&topic=b&output=rss","https://news.google.com.hk/news/feeds?region=uk&pz=1&cf=all&ned=us&hl=en&topic=b&output=rss","https://news.google.com/news/feeds?region=au&pz=1&cf=all&ned=us&hl=en&topic=b&output=rss"],
          "sports":["https://news.google.com.hk/news/feeds?region=uk&pz=1&cf=all&ned=us&hl=en&topic=s&output=rss","https://news.google.com/news/feeds?pz=1&cf=all&ned=us&hl=en&topic=s&output=rss","https://news.google.com/news/feeds?region=au&pz=1&cf=all&ned=us&hl=en&topic=s&output=rss"],
          "entertainment":["https://news.google.com/news/feeds?pz=1&cf=all&ned=us&hl=en&topic=e&output=rss","https://news.google.com.hk/news/feeds?region=uk&pz=1&cf=all&ned=us&hl=en&topic=e&output=rss","https://news.google.com/news/feeds?region=au&pz=1&cf=all&ned=us&hl=en&topic=e&output=rss"]
          
          }

zh_news={
         "international":"https://news.google.com/news/feeds?region=cn&pz=1&cf=all&ned=us&hl=zh-CN&topic=w&output=rss",
         "finance":"https://news.google.com.hk/news/feeds?region=cn&pz=1&cf=all&ned=us&hl=zh-CN&topic=b&output=rss",
         
         
         }
