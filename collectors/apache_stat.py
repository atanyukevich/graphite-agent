#!/usr/bin/env python

import urllib
import graphitestat


interval = 15

class apache_stat(graphitestat.graphitestat):
	def get_stat(self):

		result = {}
		f = urllib.urlopen('http://127.0.0.1/server-status?auto')

		for line in f.readlines():
			# {'Uptime': ' 2818294',
			# 'IdleWorkers': ' 16',
			# 'Total Accesses': ' 29089506',
			# 'Scoreboard': ' KKWK_K....',
			# 'Total kBytes': ' 124774419',
			# 'BytesPerReq': ' 4392.27',
			# 'CPULoad': ' .116002',
			# 'BytesPerSec': ' 45335.6',
			# 'ReqPerSec': ' 10.3217',
			# 'BusyWorkers': ' 88'}
			if line.split(':')[0] in ['BytesPerSec', 'ReqPerSec', 'BusyWorkers', 'IdleWorkers']:
				result['apache.' + line.split(':')[0]] = line.split(':')[1].replace('\n','')
		f.close()

		return result
