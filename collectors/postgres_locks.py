#!/usr/bin/env python

import psycopg2
import time
import graphitestat


class postgres_locks(graphitestat.graphitestat):
	def get_stat(self):
		try:
			self.conn = psycopg2.connect(host='127.0.0.1', database='monitoring', user='monitoring', password='monitoring')
			self.conn.set_session(autocommit=True, readonly=True)
			self.cur = self.conn.cursor()
		except psycopg2.Error as e:
			return None
		self.cur.execute('SELECT mode,count(*) AS count FROM pg_locks GROUP BY mode')
		measure = {}
		for tup in self.cur.fetchall():
			measure['postgres.locks.' + tup[0]] = int(tup[1])

		self.cur.close()
		self.conn.close()

		return measure


if __name__ == '__main__':
	p = postgres-locks()
	print p.get_stat()
