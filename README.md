# graphite-agent
My way to put stats into graphite

before start:
```bash
/usr/bin/getent passwd graphite || /usr/sbin/useradd -d /var/lib/graphite -m -c 'user for graphite-agent' -r -s /sbin/nologin   graphite
```
