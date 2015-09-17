#!/usr/bin/env python

import graphitestat

interval = 60

#-----------------------------------------------------------------------------#
class udp_connections(graphitestat.graphitestat):
	def get_stat(self):
		_udp_file = open('/proc/net/udp')
		udp_connections = len(_udp_file.read().split('\n'))
		_udp_file.close()
		return "net.connections.udp %d" % udp_connections
#-----------------------------------------------------------------------------#


