#! /usr/bin/python

import gzip
import sys
import pendulum
import urllib.parse
import sqlite3
from slugify import slugify


try:
    conn = sqlite3.connect(sys.argv[1])
except IndexError:
    print("Must supply a filename")
    sys.exit(1)

c = conn.cursor()

with gzip.open("backup.gz", "wb") as f:
    for row in c.execute("select name, description from task"):
        f.write(
            ",".join(
                map(
                    str,
                    [
                        "Project",
                        urllib.parse.quote(row[0]),
                        slugify(row[0]),
                        urllib.parse.quote(row[1]),
                        False,
                        False,
                        pendulum.now().isoformat(),
                        pendulum.now().isoformat(),
                    ],
                )
            ).encode("UTF-8")
            + "\n".encode("UTF-8")
        )

    for row in c.execute(
        "select task.name, timer.start, timer.stop from timer join task on timer.task_id = task.id"
    ):
        f.write(
            ",".join(
                map(
                    str,
                    [
                        "Timer",
                        slugify(row[0]),
                        pendulum.parse(row[1]).isoformat(),
                        pendulum.parse(row[2]).isoformat() if row[2] else "",
                    ],
                )
            ).encode("UTF-8")
            + "\n".encode("UTF-8")
        )
