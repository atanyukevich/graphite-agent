To be loaded by graphite-aggent module, must have:
- file with .py extension, located in /etc/graphite-collectors
- imported module graphitetest
- class named exactly as file (but without .py at the end)
- class must haw graphitestat.graphitestat class as parent
- class must contain get_stat(self) method inside. That function will be called by agent and it should be:
  * faster than 5s, otherwise agent will kill it.
  * return:
    1. string contain only "name.of_metric variable", f.e. 'load.loadavg15m 20' (only one line, so only on metric could be done by one module)
    2. dictionary, f.e.  {'load.loadavg1m':'5', 'load.loadavg5m':'4', 'load.loadavg15m':'3' } (then it will be metric by entry)
  * sender will add hostname at the beggining and timestamp at the end, before sending metrics

- class can't have __init__ method.
- module (not class), can contain 'interval' int variable, than get_stat, will be called every 'interval' seconds (by default 60)
