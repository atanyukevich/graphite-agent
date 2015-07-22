#!/usr/bin/env python

import graphitestat
import time

# man 5 proc
# /stat$
#       /proc/stat
#              kernel/system statistics.  Varies with architecture.  Common entries include:
#
#              cpu  3357 0 4313 1362393
#                     The  amount  of  time,  measured  in units of USER_HZ (1/100ths of a second on most architectures, use sysconf(_SC_CLK_TCK) to
#                     obtain the right value), that the system spent in various states:
#
#                     user   (1) Time spent in user mode.
#                     nice   (2) Time spent in user mode with low priority (nice).
#                     system (3) Time spent in system mode.
#                     idle   (4) Time spent in the idle task.  This value should be USER_HZ times the second entry in the /proc/uptime pseudo-file.
#                     iowait (since Linux 2.5.41)
#                            (5) Time waiting for I/O to complete.
#                     irq (since Linux 2.6.0-test4)
#                            (6) Time servicing interrupts.
#                     softirq (since Linux 2.6.0-test4)
#                            (7) Time servicing softirqs.
#                     steal (since Linux 2.6.11)
#                            (8) Stolen time, which is the time spent in other operating systems when running in a virtualized environment
#                     guest (since Linux 2.6.24)
#                            (9) Time spent running a virtual CPU for guest operating systems under the control of the Linux kernel.
#                     guest_nice (since Linux 2.6.33)
#                            (10) Time spent running a niced guest (virtual CPU for guest operating systems under the control of the Linux kernel).
#

interval = 59

class cpu_stat(graphitestat.graphitestat):

	def _get_stat_line(self):
		stat_file = open("/proc/stat", 'r')
		first_line = stat_file.readline().split()
		stat_file.close()
		stat_dict = {}
		if len(first_line) == 11:
			stat_dict['cpu.user'] = int(first_line[1])
			stat_dict['cpu.nice'] = int(first_line[2])
			stat_dict['cpu.system'] = int(first_line[3])
			stat_dict['cpu.iddle'] = int(first_line[4])
			stat_dict['cpu.iowait'] = int(first_line[5])
			stat_dict['cpu.irq'] = int(first_line[6])
			stat_dict['cpu.softirq'] = int(first_line[7])
			stat_dict['cpu.steal'] = int(first_line[8])
			stat_dict['cpu.guest'] = int(first_line[9])
			stat_dict['cpu.guest_nice'] = int(first_line[10])

		return stat_dict

	def _get_stat_diff(self,first_dict,second_dict):
		res_dict = {}
		for i in first_dict.keys():
			res_dict[i] = second_dict[i] - first_dict[i]
		return res_dict

	def get_stat(self):
		first_stat = self._get_stat_line()
		time.sleep(1)
		second_stat = self._get_stat_line()
		return self._get_stat_diff(first_stat,second_stat)


