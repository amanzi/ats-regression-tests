#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: clean_gold.sh DIRECTORY.regression.gold";
    exit 1
fi


cd $1
rm -f checkpoint_final.h5 *.xmf visdump_* *.stdout ats_vis_*
git add .
