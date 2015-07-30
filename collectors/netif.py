#!/usr/bin/env python

import graphitestat
import time

interval = 14


#-----------------------------------------------------------------------------#
class netif(graphitestat.graphitestat):
	def get_stat(self):
		first_state =  self.get_current_state()
		time.sleep(1)
		second_state = self.get_current_state()
		return self.get_diff_state(first_state, second_state)

	def array_to_dict(self,array):
		result = {}

	#Inter-|   Receive                                                |  Transmit
	# face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
	# odkomentowac poszczegolne errory, w razie potrzeby
		device = array[0][:-1]
		result['net.stats.' + device + '.recv.bytes'] = int(array[1])
		result['net.stats.' + device + '.recv.packets'] = int(array[2])
		result['net.stats.' + device + '.recv.errors'] = int(array[3])
		#result['net.stats.' + device + '.recv.drop'] = int(array[4])
		#result['net.stats.' + device + '.recv.fifo_errors'] = int(array[5])
		#result['net.stats.' + device + '.recv.frame_errors'] = int(array[6])
		#result['net.stats.' + device + '.recv.compressed'] = int(array[7])
		#result['net.stats.' + device + '.recv.multicast'] = int(array[8])

		result['net.stats.' + device + '.send.bytes'] = int(array[9])
		result['net.stats.' + device + '.send.packets'] = int(array[10])
		result['net.stats.' + device + '.send.errors'] = int(array[11])
		#result['net.stats.' + device + '.send.drop'] = int(array[12])
		#result['net.stats.' + device + '.send.fifo_errors'] = int(array[13])
		#result['net.stats.' + device + '.send.collisions'] = int(array[14])
		#result['net.stats.' + device + '.send.carrier_errors'] = int(array[15])
		#result['net.stats.' + device + '.send.compressed'] = int(array[16])
		return result

	def get_current_state(self):
		_tmp_file = open("/proc/net/dev")

	# biore od 3 linii, bo pierwsze 2 to naglowki tabelek
		result = {}
		for line in _tmp_file.readlines()[2:]:
			_tmp_array = line.split()
			#print _tmp_array
			_tmp_dict = self.array_to_dict(_tmp_array)
			for ind in _tmp_dict.keys():
				result[ind] = _tmp_dict[ind]

		_tmp_file.close()
		return result

	def get_diff_state(self, first_dict, second_dict):
		result = {}
		for key in first_dict.keys():
			result[key] = second_dict[key] - first_dict[key]

		return result
#-----------------------------------------------------------------------------#
