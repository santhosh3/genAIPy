import threading
import time

# x = 8192

# lock = threading.Lock()

# def double():
#     global x, lock
#     lock.acquire()
#     while x < 16384:
#         x *= 2
#         print(x)
#         time.sleep(1)
#     lock.release()
#     print('Reached the maximum')

# def halve():
#     global x, lock
#     lock.acquire()
#     while x > 1:
#         x /= 2
#         print(x)
#         time.sleep(1)
#     lock.release()
#     print('Reached the minimum')


# t1 = threading.Thread(target=double)
# t2 = threading.Thread(target=halve)

# t2.start()
# t1.start()

# ______________________________________________________________________________________

# event = threading.Event()

# def myFunction():
#     print("Waiting for event to trigger....\n")
#     event.wait()
#     print("Performing action for the event now")

# t1 = threading.Thread(target=myFunction)
# t1.start()

# x = input("Do you want to trigger event? (y/n)\n")
# if x == 'x':
#     event.set()

# ______________________________________________________________________________________

path = 'README.md'
text = ''

def readFile():
    global path, text
    while True:
        with open(path, "r") as f:
            text = f.read()
        time.sleep(2)

def printLoop():
    for x in range(20):
        print(text)
        time.sleep(1)

t1 = threading.Thread(target=readFile, daemon=True)
t2 = threading.Thread(target=printLoop)

t1.start()
t2.start()