import math
import random

def next_time(average_time):
    """ draw a time interval between two random events
    assume Poisson distribution
    """

    return -math.log(1.0 - random.random()) * average_time

def time_series(average_delta_time, N):
    """ return a list of N event times from t = 0
    assume Poission distribuition, average delta-time = average_time
    """
    t_list = [0]

    for event in range(N):
        t = next_time(average_delta_time)
        t_list.append(t+t_list[-1])

    return t_list

if __name__=="__main__":
    print "next_time.py!"
#    print "test next_time(): the value below must be near 40:"
#    print sum([next_time(40.0) for i in xrange(1000000)]) / 1000000
    print "test time_series():"
    print time_series(4,10)
