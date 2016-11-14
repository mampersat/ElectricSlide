#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import picamera
import pigpio
import sqlite3
import sys
import time
import reader
from PIL import Image


class ElectricSlide(object):

    def __init__(self):
        self.con = sqlite3.connect('electricslide.db', check_same_thread=False)

    def initialize_db(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute('CREATE TABLE users(id INT PRIMARY KEY, photo BLOB, count INT NOT NULL)')

    def close_db(self):
        self.con.close()

    def get_leaderboard(self, limit):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM users ORDER BY count desc LIMIT ?", (limit,))
            rows = cur.fetchall()
            pos = 0
            for row in rows:
                pos += 1
                print "{} - id:{} {} ({})".format(pos, row[0], row[1], row[2])
            cur.close()

    def new_user(self, user_id):
        print("HEY, You're NEW!!!!")
        try:
            camera = picamera.PiCamera()
            camera.capture('{}.jpg'.format(user_id))
        finally:
            camera.Close()

        with self.con:
            cur = self.con.cursor()
            cur.execute("INSERT INTO users VALUES(?, ?, ?)", (user_id, '{}'.format(user_id), 1))
            self.con.commit()
            cur.close()

    def ride(self, user_id):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT count from users where id=?", (user_id, ))
            try:
                count = cur.fetchone()[0]
                count += 1
                cur.execute("UPDATE users SET count=? WHERE id=?", (count, user_id))
            except TypeError:
                self.new_user(user_id)
            cur.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", help="Initialize database", action="store_true")
    args = parser.parse_args()

    slide = ElectricSlide()
    if args.init:
        slide.initialize_db()

    def callback(bits, value):
        print("bits={} value={}".format(bits, value))
        slide.ride(value)
        slide.get_leaderboard(limit=10)

    pi = pigpio.pi()
    w = reader.decoder(pi, 14, 15, callback)

    time.sleep(300)
    w.cancel()
    pi.stop()

    slide = ElectricSlide()
    slide.get_leaderboard(limit=10)
    slide.close_db()
