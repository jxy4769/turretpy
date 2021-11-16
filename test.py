import time
import throttle
n = 0

@throttle.wrap(5, 1)
def lol():
    global n
    print(n)
    n+=1

while True:
    lol()