import os
import random
import sys
import time
import logging
from boto3.session import Session
import watchtower
from logstash_formatter import LogstashFormatterV1
from itertools import count

if any("KUBERNETES" in k for k in os.environ):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(LogstashFormatterV1())

    boto3_session = Session(
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name="us-east-1")

    wt_handler = watchtower.CloudWatchLogHandler(
        boto3_session=boto3_session,
        log_group="logripper",
        stream_name="testing_with_logstashformatter")
    wt_handler.setFormatter(LogstashFormatterV1())

    logging.root.setLevel("INFO")
    logging.root.addHandler(handler)
    logging.root.addHandler(wt_handler)
else:
    logging.basicConfig(level=logging.INFO)

logga = logging.getLogger("__name__")


while True:
    for i in count():
        logga.info("Up up up! %s", i)
        if i % 1000 == 0:
            time.sleep(random.random())
        if i >= 1_000_000:
            break
    time.sleep(3600)
