#!/usr/bin/env python

import graphitestat

interval = 60

#-----------------------------------------------------------------------------#
class tcp_connections(graphitestat.graphitestat):
	def get_stat(self):
		_tcp_file = open('/proc/net/tcp')
		tcp_connections = len(_tcp_file.read().split('\n'))
		_tcp_file.close()
		return "net.connections.tcp %d" % tcp_connections
#-----------------------------------------------------------------------------#


