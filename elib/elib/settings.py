# Scrapy settings for elib project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'elib'

SPIDER_MODULES = ['elib.spiders']
NEWSPIDER_MODULE = 'elib.spiders'

USER_AGENT = 'freelib-watcher/0.1 (+https://github.com/Tigge/freelib-watcher)'

LOG_FILE="scrapy.log"
