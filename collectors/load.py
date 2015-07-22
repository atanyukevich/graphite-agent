#!/usr/bin/env python

import graphitestat

interval = 60

#-----------------------------------------------------------------------------#
class load(graphitestat.graphitestat):
	def get_stat(self):
		result = {}
		_load_file = open('/proc/loadavg')
		load_list = _load_file.read().split()[:-2]
		result['load.loadavg1m'] = load_list[0]
		# przyoszczedzenie miejsca na graphicie.. nie ma sensu rysowac 3 loady
		result['load.loadavg5m'] = load_list[1]
		result['load.loadavg15m'] = load_list[2]
		_load_file.close()
		return result
#-----------------------------------------------------------------------------#


