#!/usr/bin/env python

import urllib
from xml.dom.minidom import parseString
import graphitestat

interval=15

class vhost_stat(graphitestat.graphitestat):
	def normalize_string(self,_string):
		result=''

		for character in _string:
			# to co moze wyladowac w nazwie metryki
			if character in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
				result = result + character
			else:
				result = result + '_'
		# konwertuje do ascii, bo znaki wyzej wszystkie sa w ascii
		return result.encode('us-ascii')



	def get_stat(self):
		result = {}
		_t_file = urllib.urlopen('http://127.0.0.1/server-status')

		string = ''.join( _t_file.readlines()[1:] )

		# usuwam niezamkniety tag p oraz nowrap bez parametrow.. parser xmlliba sprawdza poprawnosc xmla a nie htmla
		xmldoc = parseString(string.replace(' nowrap','').replace('<p>',''))
		table = xmldoc.getElementsByTagName('table')[0]

		for i in table.getElementsByTagName('tr'):
			# w elemencie 11 w tabelce siedzi nazwa vhosta
			if len(i.getElementsByTagName('td')) > 11 and i.getElementsByTagName('td')[11].hasChildNodes():
				try:
					result['apache.ReqPerVhost.' + self.normalize_string(i.getElementsByTagName('td')[11].firstChild.data)] += 1
				except KeyError:
					result['apache.ReqPerVhost.' + self.normalize_string(i.getElementsByTagName('td')[11].firstChild.data)] = 1


		_t_file.close()
		return result
