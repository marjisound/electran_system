from questions.custom.question_classes.base_classes import BinaryHexBase
from questions.custom.question_classes.base_questions.interrupts_polling_dma import InterruptBase
import random


class Question(BinaryHexBase, InterruptBase):
    ANSWER_TYPE = 'multiple'
    display_correct = []
    loops_per_item = None

    def generate_user_random_display(self, value):
        return value

    def generate_random(self):

        data_transfer_cycles = random.choice([4, 6, 8])
        release_buss_cycles = random.choice([2, 4])
        data_item_bits = random.choice([8, 16, 32])
        clock_frequency = InterruptBase.clock_frequency()

        bus_clock_percentage = random.randint(1, 10)
        transfer_release_buss_microsecond = (release_buss_cycles + data_transfer_cycles) / clock_frequency
        max_kilobit_per_second = (data_item_bits / transfer_release_buss_microsecond) * 1000
        actual_data_rate = round((max_kilobit_per_second * bus_clock_percentage) / 100, 3)


        return {
            'data_transfer_cycles': data_transfer_cycles,
            'release_buss_cycles': release_buss_cycles,
            'data_item_bits': data_item_bits,
            'clock_frequency': clock_frequency,
            'actual_data_rate': actual_data_rate,
            'bus_clock_percentage': bus_clock_percentage
        }

    def expected_answer(self, value):

        max_megabits_per_second = value['data_item_bits']/(value['data_transfer_cycles']/ value['clock_frequency'])
        max_kilobits_per_second = round(max_megabits_per_second * 1000)
        bus_clock_percentage = value['bus_clock_percentage']

        return {
            'answer_data_rate': str(max_kilobits_per_second),
            'answer_bus_clock_percentage': str(bus_clock_percentage),
        }

    def test_answer(self, student_answer, correct_answer):

        diff_list = self.compare_dictionaries(student_answer, correct_answer)
        self.display_correct = diff_list

        if len(diff_list) == 0:

            return True
        else:
            return False

    def is_valid(self, student_answer):
        """
        :type student_answer: binary number string
        :rtype: dict
        """

        is_valid_data_rate, message_type_data_rate = self.is_valid_float(student_answer['answer_data_rate'])
        is_valid_bus_clock_percentage, message_type_bus_clock_percentage = self.is_valid_int(student_answer['answer_bus_clock_percentage'])

        if not is_valid_data_rate:
            if message_type_data_rate == 'format':
                self.wrong_format_message = ('Your fastest time answer did not have a correct Decimal'
                                             'format. Please try again')
            else:
                self.wrong_format_message = 'The fastest time field must be filled in. Please try again'
        elif not is_valid_bus_clock_percentage:
            if message_type_bus_clock_percentage == 'format':
                self.wrong_format_message = ('Your data rate answer did not have a correct ' 
                                             'whole number format. You need to round it if it has fraction.' 
                                             'Please try again')
            else:
                self.wrong_format_message = 'The data rate answer field must be filled in. Please try again'

        return is_valid_data_rate and is_valid_bus_clock_percentage

