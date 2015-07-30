#!/usr/bin/env python

import time
import threading
import socket
import telnetlib
import Queue

EXEC_TIMEOUT=5


#-----------------------------------------------------------------------------#
class TimeLimitExpired(Exception): pass
#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
def timelimit(func, args=(), kwargs={}):
	class FuncThread(threading.Thread):
		def __init__(self):
			threading.Thread.__init__(self)
			self.result = None

		def run(self):
			try:
				self.result = func(*args, **kwargs)
			except Exception as e:
				raise e

	it = FuncThread()
	it.start()
	it.join(EXEC_TIMEOUT)
	if it.isAlive():
		#it.stop()
		it._Thread__stop()
		raise TimeLimitExpired("Time out while running %s" %func)
	else:
		return it.result
#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
class graphitestat():
	def __init__(self,metric_queue,interval=60):
		self.interval = interval
		self.metric_queue = metric_queue

		class TimerThread(threading.Thread):
			def __init__(self,interval,function,metric_queue):
				self.hostname = socket.gethostname().split('.')[0]
				self.interval = interval
				self.function = function
				self.metric_queue = metric_queue
				threading.Thread.__init__(self)
				self.result = None
			def run(self):
				while True:
					try:
						time.sleep(self.interval)
						self.result = timelimit(self.function)
						#TODO: sending results to graphite
						if not self.result:
							continue
						if isinstance(self.result,dict):
							for i in self.result.keys():
								self.metric_queue.put( "%s.%s %s %d" \
										%(self.hostname, i, self.result[i], int(time.time())) )
						else:
							self.metric_queue.put( "%s.%s %d" %(self.hostname, self.result, int(time.time())) )

					except TimeLimitExpired as e:
						print e
					except Exception as e:
						print "smth wrong: ", e

		while_thr = TimerThread(self.interval,self.get_stat,self.metric_queue)
		while_thr.setDaemon(True)
		while_thr.start()


		if not self.get_stat:
			raise AttributeError("get_stat(function is not defined)")
#-----------------------------------------------------------------------------#
