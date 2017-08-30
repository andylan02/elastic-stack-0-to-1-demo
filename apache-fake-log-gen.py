#!/usr/bin/python
import time
import datetime
import numpy
import random
import gzip
import sys
import argparse
from faker import Faker
from tzlocal import get_localzone

local = get_localzone()


class Switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


parser = argparse.ArgumentParser(__file__, description="Fake Apache Access Log Generator")
parser.add_argument("--output", "-o", dest='output_type', help="Write to a Log file, a gzip file or to STDOUT",
                    choices=['LOG', 'GZ', 'CONSOLE'])
parser.add_argument("--count", "-c", dest='num_lines', help="Number of lines to generate (0 for infinite)", type=int,
                    default=1)
parser.add_argument("--prefix", "-p", dest='file_prefix', help="Prefix the output file name", type=str)
parser.add_argument("--start-date", "-s", dest='start_date', help="Start date (YYYY-MM-DD)", type=str)
parser.add_argument("--days", "-d", dest='generate_days', help="Num of days to generate data for", type=int, default=1)

args = parser.parse_args()

log_lines = args.num_lines
file_prefix = args.file_prefix
output_type = args.output_type
start_date = args.start_date
generate_days = args.generate_days

faker = Faker()

timestr = time.strftime("%Y%m%d-%H%M%S")
outFileName = 'apache_log_' + timestr + '.log' if not file_prefix else file_prefix + '_' + timestr + '.log'

for case in Switch(output_type):
    if case('LOG'):
        f = open(outFileName, 'w')
        break
    if case('GZ'):
        f = gzip.open(outFileName + '.gz', 'w')
        break
    if case('CONSOLE'): pass
    if case():
        f = sys.stdout


def truncated_gauss(min_out, max_out, mu, sigma, cut_point):
    while True:
        res = random.gauss(mu, sigma)
        if mu - cut_point < res < mu + cut_point:
            return (res - (mu - cut_point)) / (2 * cut_point) * (max_out - min_out) + min_out


response = ["200", "404", "500", "301"]

verb = ["GET", "POST", "DELETE", "PUT"]

resources = ["/list", "/wp-content", "/wp-admin", "/explore", "/search/tag/list", "/app/main/posts",
             "/posts/posts/explore", "/apps/cart.jsp?appID="]

ualist = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]

today = datetime.datetime.today()
start_time = datetime.datetime.strptime(start_date, "%Y-%m-%d") if start_date \
    else datetime.datetime(today.year, today.month, today.day)

count_list = [int(log_lines / generate_days) for i in range(generate_days)]
count_list[0] += log_lines % generate_days

for i in range(generate_days):
    line_count = count_list[i]
    while line_count > 0:
        otime = start_time + datetime.timedelta(seconds=int(truncated_gauss(0, 86400, 0, 1, 2)) + (i * 86400))

        ip = faker.ipv4()
        dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
        tz = datetime.datetime.now(local).strftime('%z')
        vrb = numpy.random.choice(verb, p=[0.6, 0.1, 0.1, 0.2])

        uri = random.choice(resources)
        if uri.find("apps") > 0:
            uri += repr(random.randint(1000, 10000))

        resp = numpy.random.choice(response, p=[0.9, 0.04, 0.02, 0.04])
        byt = int(random.gauss(5000, 50))
        referer = faker.uri()
        useragent = numpy.random.choice(ualist, p=[0.5, 0.3, 0.1, 0.05, 0.05])()
        f.write('%s - - [%s %s] "%s %s HTTP/1.0" %s %s "%s" "%s"\n' % (ip, dt, tz, vrb, uri, resp, byt, referer, useragent))

        line_count = line_count - 1
