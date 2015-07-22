#!/usr/bin/env python

import graphitestat

interval = 15

#-----------------------------------------------------------------------------#
class memory(graphitestat.graphitestat):
	def get_stat(self):
		result = {}
		_mem_file= open('/proc/meminfo')

		for line in _mem_file.readlines():
			result['memory.' + line.split(':')[0]] = line.split(':')[1].replace(' ','').replace('kB\n','').replace('\n','')

		_mem_file.close()
		return result
#-----------------------------------------------------------------------------#


