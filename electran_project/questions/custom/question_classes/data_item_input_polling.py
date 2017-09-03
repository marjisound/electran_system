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

        loop_instruction = 3
        read_write_instructions = random.randint(8, 16)
        instruction_clock_cycle = random.choice([4, 5, 6, 7, 8])
        data_item_bits = random.choice([8, 16, 32])
        clock_frequency = InterruptBase.clock_frequency()
        loops_per_item = random.randrange(1000, 10001, 1000)

        polling_cycle_per_item = (loops_per_item * loop_instruction) * instruction_clock_cycle
        polling_time_per_item = polling_cycle_per_item / clock_frequency
        reading_per_item = (read_write_instructions * instruction_clock_cycle) / clock_frequency
        microsecond_per_item = polling_time_per_item + reading_per_item
        microsecond_per_bit = microsecond_per_item / data_item_bits
        kilo_bit_per_second = round(1000 / microsecond_per_bit, 6)

        return {
            'loop_instruction': loop_instruction,
            'read_write_instructions': read_write_instructions,
            'instruction_clock_cycle': instruction_clock_cycle,
            'data_item_bits': data_item_bits,
            'clock_frequency': clock_frequency,
            'kilo_bit_per_second': kilo_bit_per_second,
            'loops_per_item': loops_per_item
        }

    def expected_answer(self, value):

        total_instructions = value['loop_instruction'] + value['read_write_instructions']
        total_cycle = value['instruction_clock_cycle'] * total_instructions
        fastest_time = total_cycle / value['clock_frequency']

        data_rate = round((value['data_item_bits'] / fastest_time) * 1000)

        return {
            'answer_fastest_time': str(fastest_time),
            'answer_data_rate': str(data_rate),
            'answer_loop': str(value['loops_per_item'])
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

        is_valid_fastest_time, message_type_fastest_time = self.is_valid_float(student_answer['answer_fastest_time'])
        is_valid_data_rate, message_type_data_rate = self.is_valid_int(student_answer['answer_data_rate'])
        is_valid_loop, message_type_loop = self.is_valid_int(student_answer['answer_data_rate'])

        if not is_valid_fastest_time:
            if message_type_fastest_time == 'format':
                self.wrong_format_message = ('Your fastest time answer did not have a correct Decimal'
                                             'format. Please try again')
            else:
                self.wrong_format_message = 'The fastest time field must be filled in. Please try again'
        elif not is_valid_data_rate:
            if message_type_data_rate == 'format':
                self.wrong_format_message = ('Your data rate answer did not have a correct ' 
                                             'whole number format. You need to round it if it has fraction.' 
                                             'Please try again')
            else:
                self.wrong_format_message = 'The data rate answer field must be filled in. Please try again'

        elif not is_valid_loop:
            if message_type_loop == 'format':
                self.wrong_format_message = ('Your number of loops answer did not have a correct ' 
                                             'whole number format. You need to round it if it has fraction.' 
                                             'Please try again')
            else:
                self.wrong_format_message = 'The data rate answer field must be filled in. Please try again'

        return is_valid_fastest_time and is_valid_data_rate and is_valid_loop

