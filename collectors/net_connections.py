#!/usr/bin/env python

import graphitestat

interval = 60


#-----------------------------------------------------------------------------#
class net_connections(graphitestat.graphitestat):
	def get_stat(self):
		result = {}
		# /proc/net/{tcp,udp,tcp6,udp6,unix}
		for type in ["tcp", "udp", "tcp6", "udp6", "unix" ]:

			_stat_file_ = open('/proc/net/' + type)
			result['net.connections.' + type] = len(_stat_file_.readlines())
			_stat_file_.close()

		return result
#-----------------------------------------------------------------------------#


