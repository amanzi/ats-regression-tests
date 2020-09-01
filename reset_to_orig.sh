#!/bin/bash
cd $1
for i in `ls *_orig.xml`; do mv $i `basename $i _orig.xml`.xml; done
