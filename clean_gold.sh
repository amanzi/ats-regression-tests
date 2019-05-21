#!/bin/bash
cd $1
rm -f checkpoint_final.h5 *.xmf visdump_* *.stdout
git add .
