#!/usr/bin/env python

import graphitestat
import time

# man 5 proc
# /stat$
#       /proc/stat

#              ctxt 115315
#                     The number of context switches that the system underwent.
#
#              processes 86031
#                     Number of forks since boot.
#
#              procs_running 6
#                     Number of processes in runnable state.  (Linux 2.5.45 onward.)
#
#              procs_blocked 2
#                     Number of processes blocked waiting for I/O to complete.  (Linux 2.5.45 onward.)
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

interval = 60

class procstat(graphitestat.graphitestat):
#class procstat():

	def get_stat(self):
		stat_file = open("/proc/stat", 'r')

		stat_dict = {}
		for line in stat_file.readlines():

			if line.startswith("processes "):
				stat_dict['procs.total'] = int(line.split()[1])
			
			if line.startswith("procs_running"):
				stat_dict['procs.running'] = int(line.split()[1])

			if line.startswith("procs_blocked"):
				stat_dict['procs.blocked'] = int(line.split()[1])

			if line.startswith("ctxt"):
				stat_dict['cpustat.ctxt'] = int(line.split()[1])

			if line.startswith("cpu "):
				stat_dict['cpustat.user'] = int(line.split()[1])
				stat_dict['cpustat.nice'] = int(line.split()[2])
				stat_dict['cpustat.system'] = int(line.split()[3])
				stat_dict['cpustat.iddle'] = int(line.split()[4])
				stat_dict['cpustat.iowait'] = int(line.split()[5])
				stat_dict['cpustat.irq'] = int(line.split()[6])
				stat_dict['cpustat.softirq'] = int(line.split()[7])
				stat_dict['cpustat.steal'] = int(line.split()[8])
				stat_dict['cpustat.guest'] = int(line.split()[9])
				stat_dict['cpustat.guest_nice'] = int(line.split()[10])



		stat_file.close()
		return stat_dict



if __name__ == '__main__':
	a = procstat()
	statobj = a.get_stat()
	for i in statobj.keys():
		print i, statobj[i]
