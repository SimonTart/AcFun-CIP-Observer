import server.spiders.article as articleSpider
import server.spiders.comment as commentSpider
from time import time
# articleSpider.startSpider({
#   'type': '综合',
#   'channelId': 110,
#   'realmIds': '5,1,2,4',
# })

commentSpider.crawlCommentsByArticleId(4254222, True)
