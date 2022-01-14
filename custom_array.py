import sys
import ctypes


class Array(object):
    """ Custom Dynamic Array """

    def __init__(self):
        self._n = 0
        self._cap = 1
        self._arr = self.create_arr(self._cap)

    def __len__(self):
        return self._n

    def __getitem__(self, item):
        if 0 <= item > self._n:
            return IndexError('Index out of bounds!')

        return self._arr[item]

    def append(self, a):
        if self._n == self._cap:
            self._resize(2 * self._cap)

        self._arr[self._n] = a
        self._n += 1

    def _resize(self, _ncap):
        temp = self.create_arr(_ncap)

        for idx in range(self._n):
            temp[idx] = self._arr[idx]

        self._arr = temp
        self._cap = _ncap

    @staticmethod
    def create_arr(_ncap):
        return (_ncap * ctypes.py_object)()


if __name__ == '__main__':
    arr = Array()
    arr.append(1)
    arr.append(2)
    arr.append(3)

    print("Length of array is {}".format(len(arr)))

    print("Size of array is {} bytes".format(sys.getsizeof(arr)))
