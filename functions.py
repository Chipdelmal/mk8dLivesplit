from datetime import datetime

REFT = datetime(1900, 1, 1, 0, 0, 0, 0)


def tdToSec(tDelta):
    micro = 1000000
    tm = (tDelta.seconds) + (tDelta.microseconds / micro)
    return tm
