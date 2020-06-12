import os
import cv2
from websocket import create_connection
from threading import Thread

FIFO = "/tmp/capture_pipe"
STREAM = "ws://pi_streamer_ip_addr:8084"


class MpegSync:
    def __init__(self):
        self.sync_status = 0

    def sync(self, c):
        if self.sync_status == 0:
            if c == 0:
                self.sync_status = 1
            else:
                self.sync_status = 0
        elif self.sync_status == 1:
            if c == 0:
                self.sync_status = 2
            else:
                self.sync_status = 0
        elif self.sync_status == 2:
            if c == 1:
                self.sync_status = 3
            else:
                self.sync_status = 0
        elif self.sync_status == 3:
            if c == 0xb3:
                self.sync_status = 4
            else:
                self.sync_status = 0

        return self.sync_status == 4


class ReaderThread(Thread):
    def __init__(self, pipe):
        super(ReaderThread, self).__init__()
        self.pipe = pipe
        self.stopped = False
        self.ws = create_connection(STREAM)

    def run(self):
        synced = False
        ms = MpegSync()

        while not synced:
            s = self.ws.recv()
            for i in range(len(s)):
                if ms.sync(s[i]):
                    print("Websocket synchronized to MPEG stream boundary.")
                    synced = True
                    break

        os.write(self.pipe, bytearray([0, 0, 1, 0xb3]))
        os.write(self.pipe, s[4:])

        while True:
            try:
                os.write(self.pipe, self.ws.recv())
            except:
                print("ReaderThread: connection closed")
                os.system('kill %d' % os.getpid())

            if self.stopped:
                return

    def stop(self):
        self.stopped = True


def main():
    try:
        os.remove(FIFO)
    except (FileNotFoundError):
        pass

    os.mkfifo(FIFO)
    p = os.open(FIFO, os.O_RDWR)

    rt = ReaderThread(p)
    rt.start()

    cap = cv2.VideoCapture(FIFO)

    while True:
        ret, frame = cap.read()

        if ret == False:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow('video', frame)

    cap.release()
    cv2.destroyAllWindows()

    rt.stop()
    rt.join()
    os.remove(FIFO)


if __name__ == "__main__":
    main()
