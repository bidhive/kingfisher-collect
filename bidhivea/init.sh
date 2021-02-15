#!/bin/bash

COUNT=$1
if [ -z $COUNT ]
then
    COUNT=10
fi

cd ..
scrapy crawl australia -a from_date=2021-02-01 -a sample=$COUNT

cd bidhive
export FLASK_APP=server.py
python -m flask run