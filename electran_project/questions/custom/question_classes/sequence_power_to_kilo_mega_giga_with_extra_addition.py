from questions.custom.question_classes.base_classes import BinaryHexBase
import random
from math import floor


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        return {'random1': str(value['random1']),
                'random2': str(value['random2'])
                }

    def generate_random(self):
        random_range = random.choice(list(self.POWER_DICT))
        random_offset = random.randint(2, 9)

        if random_range == 'K':
            allowed_range = list(range(10, 20))[:4]
            random_value1 = allowed_range[0]
            random_value2 = random_value1 + random_offset

        elif random_range == 'M':
            allowed_range = list(range(20, 30))[:4]
            random_value1 = allowed_range[0]
            random_value2 = random_value1 + random_offset
        else:
            allowed_range = list(range(30, 40))[:4]
            random_value1 = allowed_range[0]
            random_value2 = random_value1 + random_offset

        return {
            'random_range': random_range,
            'random1': random_value1,
            'random2': random_value2,
            'offset': random_offset
        }

    def expected_answer(self, value):
        base_value = 0
        result = 0

        while base_value <= value['offset']:
            result += (2 ** (value['random1'] + base_value))
            base_value += 1

        result += (2 ** value['random1'])

        expected = result / (2 ** self.POWER_DICT[value['random_range']])
        if int(str(expected).split('.')[1]) == 0:
            expected = floor(expected)
        return str(expected) + value['random_range']

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '')
            formatted_answer = formatted_answer.upper()
            if formatted_answer == correct_answer:
                return True
            else:
                return False
        else:
            raise TypeError('student answer must be of type string')

    def is_valid(self, answer):
        """
        :type answer: string
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


