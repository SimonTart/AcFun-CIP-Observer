from server import server
from scheduler import scheduler

import logging
logging.basicConfig(level=logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
  scheduler.start()
  server.run(host='127.0.0.1', port=8000)
