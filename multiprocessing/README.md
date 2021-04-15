# Multiprocessing in Python

The multiprocessing package offers both local and remote concurrency, effectively side-stepping the **Global Interpreter
Lock** by using subprocesses instead of threads. Due to this, the _multiprocessing_
module allows the programmer to fully leverage multiple processors on a given machine. It runs on both Unix and Windows

```python
from multiprocessing import Pool
import os


def calculate(x):
    return x ** 3


if __name__ == '__main__':
    with Pool(os.cpu_count()) as p:
        print(p.map(calculate, [1, 2, 3]))
```

## The **Process** class

```python
from multiprocessing import Process
import os


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def helper(name):
    info('function helper')
    print('hello', name)


if __name__ == '__main__':
    info('main line')
    p = Process(target=helper, args=('yakhyo',))
    p.start()
    p.join()
```

### **When to use Pool and Process**

I think choosing an appropriate approach depends on the task in hand. The pool allows you to do multiple jobs per
process, which may make it easier to parallelize your program. If you have a million tasks to execute in parallel, you
can create a Pool with a number of processes as many as CPU cores and then pass the list of the million tasks to
pool.map. The pool will distribute those tasks to the worker processes(typically the same in number as available cores)
and collects the return values in the form of a list and pass it to the parent process. Launching separate million
processes would be much less practical (it would probably break your OS)

### **Pool Process**

On the other hand, if you have a small number of tasks to execute in parallel, and you only need each task done once, it
may be perfectly reasonable to use a separate multiprocessing.process for each task, rather than setting up a Pool.

We used both, Pool and Process class to evaluate excel expressions. Following are our observations about pool and
process class:

1. **Task number**
   As we have seen, the Pool allocates only executing processes in memory and the process allocates all the tasks in
   memory, so when the task number is small, we can use process class and when the task number is large, we can use the
   pool. In the case of large tasks, if we use a process then memory problems might occur, causing system disturbance.
   In the case of Pool, there is overhead in creating it. Hence with small task numbers, the performance is impacted
   when Pool is used.

2. **IO operations**
   The Pool distributes the processes among the available cores in FIFO manner. On each core, the allocated process
   executes serially. So, if there is a long IO operation, it waits till the IO operation is completed and does not
   schedule another process. This leads to an increase in execution time. The Process class suspends the process of
   executing IO operations and schedules another process. So, in the case of long IO operation, it is advisable to use
   process class.

### Multiprocessing - video reading from webcam

```python
from multiprocessing import Pool
import os
import cv2


def webcam(src):
    cap = cv2.VideoCapture(src)  # webcam:0 ,ip camera: 'link address'
    fps = cap.get(cv2.CAP_PROP_FPS)
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.putText(frame, f'FPS: {str(fps)}', (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
            cv2.imshow('multiprocessing', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            break


if __name__ == "__main__":
    num = os.cpu_count()
    with Pool(os.cpu_count()) as p:
        p.map(webcam, [0])
```