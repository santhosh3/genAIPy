import queue

firstInFirstOut = queue.Queue()
lastInFirstOut = queue.LifoQueue()
numbers = [1, 2, 3, 4, 5]


for number in numbers:
    firstInFirstOut.put(number)
    lastInFirstOut.put(number)

print(firstInFirstOut.get())
print(firstInFirstOut.get())
print(lastInFirstOut.get())
print(lastInFirstOut.get())

priorityQueue = queue.PriorityQueue()

priorityQueue.put((2, "Hello World"))
priorityQueue.put((11, 99))
priorityQueue.put((5, 7.5))
priorityQueue.put((1, True))

while not priorityQueue.empty():
    print(priorityQueue.get()[1])