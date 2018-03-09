import server.spiders.article as articleSpider
import server.spiders.comment as commentSpider
from server.schedule import scheduler
from time import time
from server import server

if __name__ == '__main__':
  scheduler.start()
  server.run(host='127.0.0.1', port=8000)
# start = time()
# articleSpider.cralArticlesBySection({
#   'type': '综合',
#   'channelId': 110,
#   'realmIds': '5,1,2,4',
# })
# print('cost', time() - start)

# commentSpider.crawlCommentsByArticleId(4254222, True)
