# Fake Apache Access Log Generator

This script generates a boatload of fake apache access logs very quickly.
Its useful for generating fake workloads for [data ingest](http://github.com/streamsets/datacollector) and/or analytics applications.

It can write log lines to console, to log files or directly to gzip files.

It utilizes the excellent [Faker](https://github.com/joke2k/faker/) library to generate realistic ip's, URI's etc.

***

## Basic Usage

Generate a single log line to STDOUT
```
$ python3 apache-fake-log-gen.py
```

Generate 100 log lines into a .log file
```
$ python3 apache-fake-log-gen.py -c 100 -o LOG
```

Generate 100 log lines into a .gz file
```
$ python3 apache-fake-log-gen.py -c 100 -o GZ
```

Prefix the output filename 
```
$ python3 apache-fake-log-gen.py -c 100 -o LOG -p WEB1
```

Generate log from 2018-02-01 to 2018-02-10
```
$ python3 apache-fake-log-gen.py -c 100000 -s 2018-02-01 -d 10
```

Detailed help
```
$ python3 apache-fake-log-gen.py -h
usage: apache-fake-log-gen.py [-h] [--output {LOG,GZ,CONSOLE}]
                              [--count NUM_LINES] [--prefix FILE_PREFIX]
                              [--start-date START_DATE] [--days CONTINUOUS_DAYS]

Fake Apache Access Log Generator

optional arguments:
  -h, --help            show this help message and exit
  --output {LOG,GZ,CONSOLE}, -o {LOG,GZ,CONSOLE}
                        Write to a Log file, a gzip file or to STDOUT
  --count NUM_LINES, -c NUM_LINES
                        Number of lines to generate (default 1)
  --prefix FILE_PREFIX, -p FILE_PREFIX
                        Prefix the output file name
  --start-date START_DATE, -s START_DATE
                        Start date (YYYY-MM-DD)
  --days CONTINUOUS_DAYS, -d CONTINUOUS_DAYS
                        Num of days to generate data for
```


## Requirements
* Python 3.5
* `pip install -r requirements.txt`

## License
This script is released under the [Apache version 2](LICENSE) license.
