import os
import sys
import subprocess

from ..utils import read_dirs

DEFAULT_TENDER_COUNT = 10
DEFAULT_FROM_DATE = "2021-02-01"


def run():
    print("AAAAAAAA")
    subprocess.call(
        f"scrapy crawl australia -a from_date={DEFAULT_FROM_DATE} -a sample={DEFAULT_TENDER_COUNT}",
        shell=True,
    )
    read_dirs("data")


# COUNT=$1
# if [ -z $COUNT ]
# then
#     COUNT=10
# fi

# cd ..
# scrapy crawl australia -a from_date=2021-02-01 -a sample=$COUNT

# cd bidhive
# export FLASK_APP=server.py
# python -m flask run
