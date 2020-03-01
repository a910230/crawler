from worker import Worker
from queue import SimpleQueue as Queue
import os

def main():
    NUM_WORKER = 6

    if not os.path.isdir(os.getcwd() + "\\pics"):
        os.mkdir(os.getcwd() + "\\pics")

    q = Queue()
    for i in range(3220, 3200, -1):
        q.put(f"https://www.ptt.cc/bbs/Beauty/index{i}.html")

    workers = []
    for i in range(NUM_WORKER):
        workers.append(Worker(q))

    for worker in workers:
        worker.start()

if __name__ == "__main__":
    main()
