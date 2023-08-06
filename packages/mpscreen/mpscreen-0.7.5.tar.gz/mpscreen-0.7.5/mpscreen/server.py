import os
import time
import sys
from faster_fifo import Queue
from multiprocessing import Process
import os
import select
import struct


from queue import Full, Empty


from mpscreen.components import buffer, bufferServer, line, lineServer, Vstr, Vint, SR, SL, IPC_FIFO_NAME

consoleEscape = r'\u001b\[.+m'


def decode_msg_size(size_bytes: bytes) -> int:
    return struct.unpack("<I", size_bytes)[0]


def get_message(fifo: int) -> bytes:
    """Get a message from the named pipe."""
    msg_size_bytes = os.read(fifo, 4)
    msg_size = decode_msg_size(msg_size_bytes)
    msg_content = os.read(fifo, msg_size)
    return msg_content


def _screenMainLoop(s):
    s.getTerminalSize()
    s.refresh(f=True)
    start = time.time()
    resizeCheck = int(round(time.time() * 1000))
    try:
        # Open the pipe in non-blocking mode for reading
        fifo = os.open(IPC_FIFO_NAME, os.O_RDONLY | os.O_NONBLOCK)
        try:
            # Create a polling object to monitor the pipe for new data
            poll = select.poll()
            poll.register(fifo, select.POLLIN)
            try:
                while True:

                    if (fifo, select.POLLIN) in poll.poll(500):
                        msg = get_message(fifo)
                        elem = s.getElem(msg[0])
                        if elem:
                            elem.receive(msg)
                        t = int(round(time.time() * 1000))
                        if t - s.lastRefresh > 30:
                            s.lastRefresh = t
                            s.refresh()

                    else:
                        pass
                        #s.refresh()
            finally:
                poll.unregister(fifo)
        finally:
            os.close(fifo)
    finally:
        # Delete the named pipe when the reader terminates
        os.remove(IPC_FIFO_NAME)



class Server:
    def __init__(self):
        self.state = {}
        self._p = None
        self.elems = []
        self.rows = 20
        self.columns = 80
        self.lastRefresh = 0
        self.getTerminalSize()
        if not os.path.exists(IPC_FIFO_NAME):
            os.mkfifo(IPC_FIFO_NAME)

    def start(self):
        self._p = Process(target=_screenMainLoop, args=(self,))
        self._p.start()

    def buildBuffer(self, top=None, bottom=None, height=None, color=249, background=235):
        elem_id = len(self.elems)
        element = bufferServer(top=top, bottom=bottom, height=height, color=color, background=background)
        self.elems.append(element)
        return buffer(elem_id)

    def buildLine(self, top=None, bottom=None, pattern=[''], background=40, color=50):
        elem_id = len(self.elems)
        element = lineServer(top=top, bottom=bottom, pattern=pattern, background=background, color=color)
        self.elems.append(element)
        return line(elem_id, element.variables, element.variableNames)

    def getElem(self, elem):
        if elem < len(self.elems):
            return self.elems[elem]
        return None

    def refresh(self, f=False):
        if f:
            print("\u001b[2J")
        for v in self.elems:
            v.paint(rows=self.rows, columns=self.columns, f=f)
        print('\u001b[{};0H'.format(self.rows - 1))

    def getTerminalSize(self):
        rc = []
        try:
            rc = os.popen('stty size', 'r').read().split()
        except:
            pass
        if len(rc) > 0:
            if self.rows != int(rc[0]) or self.columns != int(rc[1]):
                self.refresh(f=True)
            self.rows = int(rc[0])
            self.columns = int(rc[1])


def linePrinter(cs: line):
    t = time.time()
    while True:
        for i in range(300000):
            cs["v"].set(str(time.time()- t))
            #time.sleep(2.2)


def linePrinter2(cs: line):
    while True:
        for i in range(0, 10000):
            cs["count"].add(1)
            #time.sleep(1.2)


def bufferPrinter(bs: buffer):
    for i in range(1000, 3000):
        bs.append(('\u001b[48;5;13m') + (str(i) * (2)))
        bs.append((str(i) * 13))
        time.sleep(1.1)


if __name__ == "__main__":
    ss = Server()
    l1 = ss.buildLine(top=1, pattern=[" Main Pattern : ", SR(background=240), "  ",Vstr("v"),"  "], background=52, color=207)
    l2 = ss.buildLine(top=2, pattern=[" Main Pattern  ", SR(background=240), Vint("count:>8")," ", SR(background=245), Vint("total:>8")," "], background=55, color=207)
    upperConsole = ss.buildBuffer(top=3, height=20)
    lowerConsole = ss.buildBuffer(bottom=2, top=25, background = 117)
    ss.buildLine(top=24, background=24)
    ss.buildLine(bottom=1, background=24)
    ss.start()

    pr = [Process(target=linePrinter, args=[l1]),
          Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),
          Process(target=linePrinter2, args=[l2]), Process(target=linePrinter2, args=[l2]),

          Process(target=bufferPrinter, args=[upperConsole]),
          Process(target=bufferPrinter, args=[lowerConsole])
    ]

    for p in pr:
        p.start()

    for p in pr:
        p.join()

