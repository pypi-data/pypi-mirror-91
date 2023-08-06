import time
from threading import Thread


def sleep_a_bit():
    time.sleep(1)


def main():
    t = Thread(target=sleep_a_bit)
    t.start()
    t.join()


main()
