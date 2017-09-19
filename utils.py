import time

def recordJobCoastTime(func, jobName, **args):
  def wrapFunc():
    print('[Job Begin]:', jobName)
    beginTime = time.time()
    func(**args)
    endTime = time.time()
    cost = str(endTime - beginTime)
    print('[Job End]: {0}, Coast: {1}s'.format(jobName, cost))
  return wrapFunc