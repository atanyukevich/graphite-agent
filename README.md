# graphite-agent
My way to put stats into graphite

before start:
```bash
/usr/bin/getent passwd graphite || /usr/sbin/useradd -d /var/lib/graphite -m -c 'user for graphite-agent' -r -s /sbin/nologin   graphite
```

## How it works
- at start graphiteagent loads all modules from /etc/graphite-collectors
- starts separate thread for every module with
```python
while True:
	sleep(interval)
```
- when sleep ends, it starts another thread with get_stat() function, and kill it after 5s if function doesn't finish before
- and there is one more thread sends metrics into graphite which is configured in graphiteagent with global variables (TODO: move into config)
- after 5 fails sys.exit raises, and unit restarts whole daemon.
- results of get_stat() are pushed into queue to send, with timestamp and hostname appended (TODO: add PREFIX, and SUFFIX settings)
- if get_stat returns dictionary, it appends, timestamp and hostname to each.
- so example module:

```python
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
```
