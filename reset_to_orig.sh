#!/bin/bash
cd $1
rm -rf $2.regression $2.regression.gold
mv $2_orig.xml $2.xml
