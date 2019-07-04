# SimLog
Utility to store the commandline of each runs and the result status at a remote webserver. The webserver is communicated through UDP so that the user wouldn't be affected, even if the webserver is not _UP_.

More information at my [webpage](https://narenkn.com/works/verif/simlog.html).

## Dependencies
```bash
sudo apt install cython
```

## Debug
During debug mode, set SIMLOG_DEBUGON environment variable.

## Build
```bash
make PY=/tools/pandora64/.package/python-2.6.2/bin/python
```

## Cron Commands
```bash
*/5 * * * * cd /proj/lna_verif_workarea/users/naren/try/junk/simlog/simlog_run && bash ../src/simlog_srv.sh
0   * * * * python /proj/lna_verif_workarea/users/naren/try/junk/simlog/utils/save.py
0   0 * * * python /proj/lna_verif_workarea/users/naren/try/junk/simlog/utils/quit.py
```
