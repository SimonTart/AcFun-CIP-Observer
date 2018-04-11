from server import server
import logging
from server.schedule import scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

if __name__ == '__main__':
    scheduler.start()
    server.run(host='127.0.0.1', port=8000)