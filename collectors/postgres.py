#!/usr/bin/env python

import psycopg2
import time
import graphitestat


class postgres(graphitestat.graphitestat):
	def get_stat(self):
		try:
			self.conn = psycopg2.connect(host='127.0.0.1', database='monitoring', user='monitoring', password='monitoring')
			self.conn.set_session(autocommit=True, readonly=True)
			self.cur = self.conn.cursor()
		except psycopg2.Error as e:
			return None

		self.row_list = ['numbackends', 'xact_commit', 'xact_rollback', 'blks_read', 'blks_hit', \
				'tup_returned', 'tup_fetched', 'tup_inserted', 'tup_updated', 'tup_deleted', \
				'conflicts', 'temp_files', 'temp_bytes', 'deadlocks']

		first_result = {}
		first_result = self.get_sum_dict(self.cur, 'pg_stat_database', self.row_list )

		time.sleep(1)

		second_result = {}
		second_result = self.get_sum_dict(self.cur, 'pg_stat_database', self.row_list)

		self.cur.close()
		self.conn.close()

		return self.get_diff(first_result, second_result)

	def get_sum_dict(self, cursor, table, row_list=[]):
		result = {}
		_tmp_select = "SELECT"
		for row in row_list:
			_tmp_select = _tmp_select + ' sum(%s),' % row

		_tmp_select = _tmp_select[:-1] + ' FROM %s ;'%table

		cursor.execute(_tmp_select)
		_tmp_tupple = cursor.fetchone()

		for _tmp_var in  _tmp_tupple:
			result['postgres.' + row_list[_tmp_tupple.index(_tmp_var)]] = int(_tmp_var)

		return result


	def get_diff(self, first_dict, second_dict):
		result = {}
		for key in first_dict.keys():
			if key == 'postgres.numbackends':
				result[key] = int(max(second_dict[key],first_dict[key]))
			else:
				result[key] = int(second_dict[key] - first_dict[key])

		return result

