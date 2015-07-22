Dla zaladowanie przez grapthie-agenta modul musi miec:

	- pliczek o nazwie modulu i '.py' na koncu w katalogu /etc/graphite-collectors
	- zaimportowany modul graphitestat
	a w srodku:
	- classa nazywajaca sie dokladnie tak samo jak modul (nazwa plicku bez .py)
	- classa musi dziedziczyc po graphitestat.graphitestat
	- classa musi miec metode get_stat(self). Ta metoda bedzie wolana przez agenta i musi byc na tyle ogarnieta, ze:
		nie moze trwac wiecej niz 5 sekund, inaczej ubicie i cala praca w las
		zwracac stringa typu: 'load.loadavg1m 5' (jedna linijka, za tym idzie tylko jeden pomiar)
		albo zwracac slownik: {'load.loadavg1m':'5', 'load.loadavg5m':'4', 'load.loadavg15m':'3' } (wtedy bedzie pomiar per wpis...)
		wysylacz tego co zwraca metota get_stat(), doklei hostname'y sprzodu i timestampy na koncua
	- jesli classa musi zawierac metode __init__(): ,to trzeba odpalic nadrzednego __init__ z graphitestat'a
	- jesli modul bedzie zawieral zmienna interval(liczba) to metoda get_stat() bedzie wolana co 'interval' sekund, jesli nie, to co 60s.
	- classa moze zawierac inne metody do pomocy ale wolana bedzie tylko get_stat(). natomiast uzywanie innych metod wewnatrz classy jakto zawsze wewnatrz classy self.metoda, ale z get_stat()'a

jak to dziala:
	- przy starcie sa ladowane wszystkie moduly
	-  dla kazdego modulu jest odpalany swoj watek z while True: sleep(interval)
	- jak sie konczy sleep, to jest odpalany kolejny watek a w nim funkcja get_stat() i ten watek jest ubijany po 5 skundach, jesli nie skonczy sam
	- oraz odpalany jest jeszcze jeden watek, ktory odpowiada za wyslanie pomiarow do centrali. (co sekunde bierze stringi z kolejki do wyslania i wysyla)
	- po 5 nieudanych probach wyslania pomiaru zdycha calosc. A unit ma restart on failure....
	- wyniki get_stata sa wypychane na kolejke po jednym po doklejeniu hostname'a timestamp'a oraz rozdzieleniu slownikow na pojedyncze pomiary.

no i przykladowy modul:



$ cat load.py
#!/usr/bin/env python

import graphitestat

interval = 60

#-----------------------------------------------------------------------------#
class load(graphitestat.graphitestat):
	def get_stat(self):
		result = {}
		_load_file = open('/proc/loadavg')
		load_list = _load_file.read().split()[:-2]
		result['load.loadavg1m'] = load_list[0]
		result['load.loadavg5m'] = load_list[1]
		result['load.loadavg15m'] = load_list[2]
		_load_file.close()
		return result
#-----------------------------------------------------------------------------#



