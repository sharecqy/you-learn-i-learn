# Scrapy settings for baidu_jangtang project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'baidu_jangtang'

SPIDER_MODULES = ['baidu_jangtang.spiders']
NEWSPIDER_MODULE = 'baidu_jangtang.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'baidu_jangtang (+http://www.yourdomain.com)'

DEPTH_LIMIT=10
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

USER_AGENT = "Mozilla/6.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22 AlexaToolbar/alxg-3.1"


ITEM_PIPELINES = [
    'baidu_jangtang.pipelines.BaikeExtractPipeline',
    'baidu_jangtang.pipelines.BaikeStorePipeline',
    'baidu_jangtang.pipelines.ZhidaoExtractPipeline',    
    'baidu_jangtang.pipelines.ZhidaoStorePipeline',
]

DOWNLOAD_DELAY = 4
REDIRECT_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'baidu_jangtang.RotateUserAgentMiddleware.RotateUserAgentMiddleware' :400}
COOKIES_DEBUG=True