from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        return value

    def generate_random(self):
        start_track = random.randrange(100, 1000, 100)
        track = random.randrange(1100, 14792)
        track_seek = random.randint(5, 10)
        sector_numbers = random.choice([300, 400, 500])
        read_sectors = random.randrange(10, 101, 10)
        random_rpm = random.randrange(1000, 20000, 100)

        return {'start_track': start_track,
                'track': track,
                'track_seek': track_seek,
                'sector_numbers': sector_numbers,
                'read_sectors': read_sectors,
                'random_rpm': random_rpm}

    def expected_answer(self, value):

        move_to_track = value['track_seek']
        rotational_latency = round((60000 / value['random_rpm']) / 2, 3)
        read_sectors = round(((60000 / value['random_rpm']) / value['sector_numbers'])*value['read_sectors'], 3)

        result = round(move_to_track+rotational_latency+read_sectors, 2)

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

