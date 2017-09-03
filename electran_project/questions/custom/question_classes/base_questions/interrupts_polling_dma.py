import random
import codecs
import os


class InterruptBase:

    @staticmethod
    def clock_frequency():
        base_digit = random.choice([1, 2, 5])
        zero_amount = random.randrange(3)

        return int(str(base_digit) + (zero_amount * str(0)))