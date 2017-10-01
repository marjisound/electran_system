from questions.custom.question_classes.base_classes import BinaryHexBase
import random
from math import floor


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        return {'random1': str(value['random1']),
                'random2': str(value['random2']),
                'random3': str(value['random3'])
                }

    def generate_random(self):
        random_range = random.choice(list(self.POWER_DICT))

        if random_range == 'K':
            random_value = self.generate_three_different_random_in_range(10, 20)

        elif random_range == 'M':
            random_value = self.generate_three_different_random_in_range(20, 30)
        else:
            random_value = self.generate_three_different_random_in_range(30, 40)

        random_value['random_range'] = random_range

        return random_value

    @staticmethod
    def generate_three_different_random_in_range(lower_range, upper_range):
        allowed_range = list(range(lower_range, upper_range))

        random_value1 = random.choice(allowed_range)
        allowed_range.remove(random_value1)

        random_value2 = random.choice(allowed_range)
        allowed_range.remove(random_value2)

        random_value3 = random.choice(allowed_range)

        return {'random1': random_value1, 'random2': random_value2, 'random3': random_value3}

    def expected_answer(self, value):
        expected = ((2 ** value['random1']) + (2 ** value['random2']) + (2 ** value['random3']))
        expected /= (2 ** self.POWER_DICT[value['random_range']])
        if int(str(expected).split('.')[1]) == 0:
            expected = floor(expected)
        return str(expected) + value['random_range']

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '')
            formatted_answer = formatted_answer.replace('\t', '')
            formatted_answer = formatted_answer.upper()
            if formatted_answer == correct_answer:
                return True
            else:
                return False
        else:
            raise TypeError('student answer must be of type string')

    def is_valid(self, answer):
        """
        :type hex_num: hex number string
        :rtype: dict
        """

        if not answer or type(answer) != str:
            self.wrong_format_message = 'The answer field must be filled in. Please try again'
            is_valid = False
        else:
            formatted_answer = answer.upper()
            unit_exist = False
            for item in list(self.POWER_DICT):
                if item in formatted_answer:
                    unit_exist = True
            if not unit_exist:
                self.wrong_format_message = 'Your answer did not have a K, M or G sign for unit type. Please try again'
                is_valid = False
            else:
                is_valid = True

        return is_valid


