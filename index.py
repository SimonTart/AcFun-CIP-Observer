from server import server
from server.schedule import scheduler

if __name__ == '__main__':
  scheduler.start()
  server.run(host='127.0.0.1', port=8000)