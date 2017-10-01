from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        return value

    def generate_random(self):

        random_rpm = random.randrange(1000, 20000, 100)

        return {'random1': random_rpm}

    def expected_answer(self, value):

        result = round((60000 / value['random1']) / 2, 2)

        return result

    def test_answer(self, student_answer, correct_answer):

        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '').replace('\t', '')

            if float(formatted_answer) == correct_answer:
                return True
            else:
                return False
        else:
            raise TypeError('student answer must be of type string')

    def is_valid(self, student_answer):
        """
        :type student_answer: binary number string
        :rtype: dict
        """
        is_valid, message_type = self.is_valid_float(student_answer)
        if not is_valid:
            if message_type == 'format':
                self.wrong_format_message = 'Your answer did not have a correct decimal format. Please try again'
            else:
                self.wrong_format_message = 'The answer field must be filled in. Please try again'

        return is_valid

