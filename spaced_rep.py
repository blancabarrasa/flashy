import datetime, random


def next_spaced_rep(stage, last):
    increment = (stage * 2) + 1
    next = last + datetime.timedelta(days=increment)
    return next



