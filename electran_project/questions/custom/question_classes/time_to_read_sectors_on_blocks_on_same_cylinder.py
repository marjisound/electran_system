from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        return value

    def generate_random(self):
        track_numbers = 14000
        tracks_in_cylinder = random.randint(4, 12)
        sectors_in_block = random.randrange(4, 17, 4)
        sector_numbers = random.choice([300, 400, 500])
        read_sectors = random.randrange(20, 101, 10)
        random_rpm = random.randrange(1000, 20000, 100)

        return {'track_numbers': track_numbers,
                'tracks_in_cylinder': tracks_in_cylinder,
                'sectors_in_block': sectors_in_block,
                'sector_numbers': sector_numbers,
                'read_sectors': read_sectors,
                'random_rpm': random_rpm}

    def expected_answer(self, value):

        number_of_blocks = int(value['read_sectors'] / value['sectors_in_block'])
        remaining_sectors = value['read_sectors'] % value['sectors_in_block']

        rotational_latency = round((60000 / value['random_rpm']) / 2, 3)
        time_read_block = round(((60000 / value['random_rpm']) / value['sector_numbers']) * value['sectors_in_block'], 3)

        if remaining_sectors > 0:
            time_read_remaining = round(((60000 / value['random_rpm']) / value['sector_numbers']) * remaining_sectors,
                                        3)
            result = round(
                (number_of_blocks * (rotational_latency + time_read_block)) + (
                 rotational_latency + time_read_remaining
                ), 2)
            expected = {'result': result,
                        'number_of_blocks': number_of_blocks,
                        'rotational_latency': rotational_latency,
                        'time_read_block': time_read_block,
                        'time_read_remaining': time_read_remaining,
                        'remaining_sectors': remaining_sectors}
        else:
            result = round(
                (number_of_blocks * (rotational_latency + time_read_block)), 2)
            expected = {'result': result,
                        'number_of_blocks': number_of_blocks,
                        'rotational_latency': rotational_latency,
                        'time_read_block': time_read_block}

        return expected

    def test_answer(self, student_answer, correct_answer):

        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '')

            if float(formatted_answer) == correct_answer['result']:
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

