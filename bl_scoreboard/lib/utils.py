# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from datetime import timedelta


def timedelta_to_str(tmd):
    if tmd is None:
        return u""
    min_sec = divmod(tmd.seconds, 60)
    tmd_str = u"{:02d}:{:02d}:{:02d}".format(*(min_sec + (tmd.microseconds/10000,)))
    return tmd_str


def str_to_timedelta(st):
    tm = [float(x) for x in st.split(u":")]
    for i in xrange(0, 3-len(tm)):
        tm.insert(0, 0)
    tmd = timedelta(minutes=tm[0], seconds=tm[1], microseconds=tm[2]*10000)
    return tmd