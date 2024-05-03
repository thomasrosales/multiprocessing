from threading import Thread


class SquaredSumWorker(Thread):

    def __init__(self, n, **kwargs):
        super().__init__(**kwargs)
        self._n = n
        self.start()

    def _calculate_sum_squares(self):
        sum_squares = 0
        for index in range(self._n):
            sum_squares += index**2

        print(sum_squares)

    def run(self):
        self._calculate_sum_squares()
