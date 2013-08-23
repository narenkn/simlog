.PHONY: all clean getfiles syncdn syncup

PY = /usr/bin/python

CFLAGS = -Duint32=unsigned
CCC = g++
CC = gcc

all: utils/memfrob src/simlog.S simlog.py.c simlog.py.S simlog.py.exe simlog

clean:
	-\rm -f save_file_20032011.pkl  simlog  simlog.exml src/simlog.S simlog.py.c utils/memfrob simlog.py.S

%.S : %.cc
	$(CCC) $(CFLAGS) -S -o $@ $<

%.pyc :
	PYTHONPATH=src $(PY) -c "import $*"

simlog: src/simlog.S utils/main.cc
	$(CCC) -o $@ $+

SOURCE_FILES = ./utils/main.cc ./utils/save.py ./utils/print_table.py ./utils/quit.py ./utils/memfrob.c ./simlog_run/simlog_26_03_2011.log ./Makefile ./sim_results.xml ./src/simlog.py ./src/simlog_srv.sh ./src/simlog.cc ./src/simlog_srv.py ./README

%.py.c : src/%.py
##	scp -f idclogin01:/proj/lna_verif_workarea/users/naren/try/junk/simlog/src/simlog.py src/simlog.py
	cython --embed -o $@ $<

%.py.S : %.py.c
	$(CC) `$(PY) -c 'from distutils.sysconfig import *; print "-I"+get_python_inc()+" ";'` -S $< -o $@

%.py.exe : %.py.S
	$(CC) `$(PY) -c 'from distutils.sysconfig import *; print "-I"+get_python_inc()+" ";'` $< `$(PY) -c 'import re; from distutils.sysconfig import *; d = get_config_vars(); t = d["LIBRARY"]; t = re.sub("lib","",t); t = re.sub(".a","",t); print "-l"+t,; print d["LIBS"],;'` -lm -o $@

