#!/usr/bin/env python

import time
import graphitestat

# every 14 second + 1 second sleep to count diffs
interval = 14


# /proc/diskstats https://github.com/torvalds/linux/blob/master/Documentation/iostats.txt
#
#Field  1 -- # of reads completed
#    This is the total number of reads completed successfully.
#Field  2 -- # of reads merged, field 6 -- # of writes merged
#    Reads and writes which are adjacent to each other may be merged for
#    efficiency.  Thus two 4K reads may become one 8K read before it is
#    ultimately handed to the disk, and so it will be counted (and queued)
#    as only one I/O.  This field lets you know how often this was done.
#Field  3 -- # of sectors read
#    This is the total number of sectors read successfully.
#Field  4 -- # of milliseconds spent reading
#    This is the total number of milliseconds spent by all reads (as
#    measured from __make_request() to end_that_request_last()).
#Field  5 -- # of writes completed
#    This is the total number of writes completed successfully.
#Field  6 -- # of writes merged
#    See the description of field 2.
#Field  7 -- # of sectors written
#    This is the total number of sectors written successfully.
#Field  8 -- # of milliseconds spent writing
#    This is the total number of milliseconds spent by all writes (as
#    measured from __make_request() to end_that_request_last()).
#Field  9 -- # of I/Os currently in progress
#    The only field that should go to zero. Incremented as requests are
#    given to appropriate struct request_queue and decremented as they finish.
#Field 10 -- # of milliseconds spent doing I/Os
#    This field increases so long as field 9 is nonzero.
#Field 11 -- weighted # of milliseconds spent doing I/Os
#    This field is incremented at each I/O start, I/O completion, I/O
#    merge, or read of these stats by the number of I/Os in progress
#    (field 9) times the number of milliseconds spent doing I/O since the
#    last update of this field.  This can provide an easy measure of both
#    I/O completion time and the backlog that may be accumulating.

#-----------------------------------------------------------------------------#
class iostat(graphitestat.graphitestat):

	def diskstats_table_to_dict(self,table):
		''' Assignes name to table fields '''

		result = {}

		device = table[2]

		result['iostat.' + device + '.reads'] = int(table[3])
		result['iostat.' + device + '.reads_merged'] = int(table[4])
		result['iostat.' + device + '.sectors_read'] = int(table[5])
		result['iostat.' + device + '.time_read'] = int(table[6])

		result['iostat.' + device + '.writes'] = int(table[7])
		result['iostat.' + device + '.writes_merged'] = int(table[8])
		result['iostat.' + device + '.sectors_written'] = int(table[9])
		result['iostat.' + device + '.time_write'] = int(table[10])

		result['iostat.' + device + '.current_io_count'] = int(table[11])

		return (device,result)

	def get_whole_diskstats(self):
		_tmp_file = open('/proc/diskstats')

		result = []

		for i in _tmp_file:
			result.append( self.diskstats_table_to_dict( i.split() ) )

		_tmp_file.close()
		return result

	def diff_diskstats(self,first,second):
		result = {}

		for i in first[1].keys():
			result[i]= second[1][i] - first[1][i]

		return result


	def diff_whole_diskstats(self,first, second):
		result = {}
		for i in first:
			for tmp_key in self.diff_diskstats(i,second[first.index(i)]).keys():
				result[tmp_key] = self.diff_diskstats(i,second[first.index(i)])[tmp_key]

		return result


	def get_stat(self):
		first_snap = self.get_whole_diskstats()
		time.sleep(1)
		second_snap = self.get_whole_diskstats()

		return self.diff_whole_diskstats(first_snap,second_snap)
#-----------------------------------------------------------------------------#








