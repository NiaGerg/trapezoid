import multiprocessing
import random as rd
import time
import threading


"""with threads Finished in:  0.01 second(s)
with pools Finished in:  0.17 second(s)
Hybrid execution Finished in:  0.32 second(s)"""


class Trapezoid:

    def __init__(self, trap=[0, 0, 0]):
        self.a = min(trap)
        self.b = max(trap)
        self.h = sum(trap) - self.a - self.b

    def __str__(self):
        return 'Trapezoid: Big Base -> {}, Small Base -> {}, Height -> {}'.format(self.b, self.a, self.h)

    def area(self):
        return (self.a + self.b) / 2 * self.h

    def __lt__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() < other.area()
        return False

    def __eq__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() == other.area()
        return False

    def __ge__(self, other):
        if isinstance(other, Trapezoid):
            return not self.__lt__(other)
        return False

    def __add__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() + other.area()
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Trapezoid):
            return abs(self.area() - other.area())
        return NotImplemented

    def __mod__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() / other.area()
        return NotImplemented


# creating rectangle class which is child of trapezoid
class Rectangle(Trapezoid):
    def __init__(self, re=None):
        if re is None:
            re = [0, 0]
        super().__init__([re[0], re[0], re[1]])

    def __str__(self):
        return "Rectangle: Width -> {}, Height -> {}".format(self.a, self.h)


# creating square class which is child of rectangle
class Square(Rectangle):
    def __init__(self, c):
        super().__init__([c, c, c])

    def __str__(self):
        return "Square: Side Length -> {}".format(self.a)


# functions to calculate generate areas
def trapezoid_area(arr):
    for i in arr:
        t = Trapezoid(i)
        t.area()


def rectangle_area(arr):
    for i in arr:
        r = Rectangle(i)
        r.area()


def square_area(arr):
    for i in arr:
        s = Square(i)
        s.area()


# this function is used to calculate time to compute areas of 10000 trapezoid,
# rectangle and square in general without threads or processes
def regular(arr):
    start = time.perf_counter()

    trapezoid_area(arr)
    rectangle_area(arr)
    square_area(arr)

    finish = time.perf_counter()

    print('in general Finished in: ', round(finish - start, 2), 'second(s)')


# this function is used to calculate time to compute areas of 10000 trapezoid, rectangle and square using threads
def threads(arr):
    start1 = time.perf_counter()

    t1 = threading.Thread(target=trapezoid_area, args=(arr,))
    t1.start()
    t2 = threading.Thread(target=rectangle_area, args=(arr,))
    t2.start()

    t1.join()
    t2.join()

    finish1 = time.perf_counter()
    print('with threads Finished in: ', round(finish1 - start1, 2), 'second(s)')


def multiprocess(arr):
    start2 = time.perf_counter()

    p1 = multiprocessing.Process(target=trapezoid_area, args=(arr,))
    p2 = multiprocessing.Process(target=rectangle_area, args=(arr,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    finish2 = time.perf_counter()
    print('with pools Finished in: ', round(finish2 - start2, 2), 'second(s)')


def hybrid(arr):
    start3 = time.perf_counter()
    processes = []

    for _ in range(5):
        p = multiprocessing.Process(target=process_with_threads, args=(arr,))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    finish3 = time.perf_counter()
    print('Hybrid execution Finished in: ', round(finish3 - start3, 2), 'second(s)')


def process_with_threads(arr):
    for _ in range(20):
        t = threading.Thread(target=trapezoid_area, args=(arr,))
        t.start()
        t.join()


if __name__ == "__main__":
    trapecoids = [[rd.randint(1, 200), rd.randint(1, 200), rd.randint(1, 200)] for _ in range(10000)]
    rectangles = [[rd.randint(1, 200), rd.randint(1, 200)] for _ in range(10000)]
    squars = [rd.randint(1, 200) for _ in range(10000)]

    threads(trapecoids)
    multiprocess(trapecoids)
    hybrid(trapecoids)
