from contextlib import contextmanager
import sys
import time


class Tqdm:
    """
    Initiates a class that wraps iterable objects, and presents information regarding the iteration progress.
    """

    def __init__(self, iterable):
        """
        Initiates the wrapper class.

        :param iterable: The iterable on which information will be provided during iteration.
        """
        self.iterable = iter(iterable)
        self.iterations_limit = len(iterable)
        self.iteration_number = 1
        self.iteration_start_time = None
        self.iterations_per_second = 0
        # Clear_the_screen.
        sys.stdout.write("\u001b[1J")
        # Move to line 2 of the screen, so the first line is free for the task bar.
        sys.stdout.write("\u001b[2;0f")

    def __iter__(self):
        return self

    def __next__(self):
        """
        Provides statistics regarding the iteration progress, and calls the next object of the iterator.
        :return: The next object of the iterator.
        """
        if self.iteration_number == 1:
            self.iteration_start_time = time.monotonic()
        self.print_iteration_status()
        self.iteration_number += 1
        return next(self.iterable)

    def print_iteration_status(self):
        """
        Print statistics regarding the iteration progress.
        """
        if self.iteration_number <= self.iterations_limit:
            percent_completed = int(self.iteration_number / (self.iterations_limit) * 100)
            if self.iteration_number != 1:
                self.iterations_per_second = self.iteration_number / self.elapsed_time
        else:
            percent_completed = 100
            self.iteration_number = self.iterations_limit
        with self.write_first_line():
            print(f"Iteration Number: {self.iteration_number}/{self.iterations_limit}",
                  "Elapsed Time:{:7.4f}".format(self.elapsed_time),
                  "Iterations Per Second:{:7.4f}".format(self.iterations_per_second),
                  "Completed: {:>3s}%".format(str(percent_completed)),
                  "[{:10s}]".format("#" * (percent_completed // 10)))

    @property
    def elapsed_time(self)->float:
        """
        Calculates the elapsed time starting from the first iteration.
        :return: Time since the first iteration
        """
        return time.monotonic() - self.iteration_start_time

    @staticmethod
    @contextmanager
    def write_first_line():
        """
        A context manager that allows us to write to thw first line of the terminal, and return to the current cursor
        position.
        """
        try:
            sys.stdout.write("\u001b[s")
            sys.stdout.write("\u001b[0;0f")
            yield
        finally:
            sys.stdout.write("\u001b[u")


def main():
    for i in Tqdm(range(10)):
        print(i)
        time.sleep(1)


if __name__ == '__main__':
    main()
