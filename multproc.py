import multiprocessing
import time


def proc1_func():
    time.sleep(1)
    print("sup1")
def proc2_func():
    time.sleep(2)
    print("sup2")



proc1 =  multiprocessing.Process(target=proc1_func)
proc2 =  multiprocessing.Process(target=proc2_func)

proc1.start()
proc2.start()
