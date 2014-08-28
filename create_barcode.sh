#!/bin/bash
nohup ls -1 profile/* | xargs -l -i --max-procs=`grep -c '^processor' /proc/cpuinfo` Rscript create_barcode.R {} barcode/ &>/dev/null &
