import time
import logging


def recordJobCoastTime(func, jobName, **args):
  logger = logging.getLogger(jobName)
  def wrapFunc():
    logger.info('[Job Begin]:%s', jobName)
    beginTime = time.time()
    func(jobName, **args)
    endTime = time.time()
    cost = str(endTime - beginTime)
    logger.info('[Job End]: %s, Coast: %s', jobName, cost)
  return wrapFunc