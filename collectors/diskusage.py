#!/usr/bin/env python

import graphitestat
import os

interval = 300

#  os.statvfs(path)
#	The return value is an object whose attributes describe the filesystem on the given path,
#	and correspond to the members of the statvfs structure, namely:
#	f_bsize, f_frsize, f_blocks, f_bfree, f_bavail, f_files, f_ffree, f_favail, f_flag, f_namemax.

#-----------------------------------------------------------------------------#
class diskusage(graphitestat.graphitestat):

	def _normalize_name(self,string):
		string = string[1:]
		if not string:
			string = 'root'
		return string.replace('/', '_').replace('.','_')

	def get_stat(self):
		_tmp_file = open('/proc/mounts', 'r')
		result = {}
		for line in _tmp_file.readlines():
			vfs=line.split()
			if vfs[0][0] == '/':
				stat = os.statvfs(vfs[1])
				result['diskusage.' + self._normalize_name(vfs[1]) + '.bytes_used'] = (stat.f_blocks - stat.f_bavail ) * stat.f_bsize
				result['diskusage.' + self._normalize_name(vfs[1]) + '.bytes_total'] = stat.f_blocks * stat.f_bsize
				result['diskusage.' + self._normalize_name(vfs[1]) + '.inodes_used'] = stat.f_files - stat.f_favail
				result['diskusage.' + self._normalize_name(vfs[1]) + '.inodes_total'] = stat.f_files

		_tmp_file.close()
		return result
#-----------------------------------------------------------------------------#
