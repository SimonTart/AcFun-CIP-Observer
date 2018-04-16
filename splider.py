import logging
from server.schedule import scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

if __name__ == '__main__':
    scheduler.start()