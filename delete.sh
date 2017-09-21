#!/bin/bash

#  Delete directories recursively if date modified is greater than 30 days.
for i in $(ls -d -- */)
    do find ./$i -maxdepth 1 -type d -ctime +30 -exec rm -rf {} \;
done
