from questions.custom.question_classes.base_classes import BinaryHexBase
from questions.custom.question_classes.base_questions.interrupts_polling_dma import InterruptBase
import random


class Question(BinaryHexBase, InterruptBase):
    ANSWER_TYPE = 'multiple'
    display_correct = []

    def generate_user_random_display(self, value):
        return value

    def generate_random(self):

        interrupt_clock_cycle = random.choice([5, 10, 15, 20])
        isr_instructions = random.randrange(10, 101, 10)
        instruction_clock_cycle = random.choice([4, 5, 6, 7, 8])
        data_item_numbers = random.randrange(2, 13, 2)
        data_item_bits = random.choice([8, 16, 32])
        clock_frequency = InterruptBase.clock_frequency()

        return {
            'interrupt_clock_cycle': interrupt_clock_cycle,
            'isr_instructions': isr_instructions,
            'instruction_clock_cycle': instruction_clock_cycle,
            'data_item_numbers': data_item_numbers,
            'data_item_bits': data_item_bits,
            'clock_frequency': clock_frequency
        }

    def expected_answer(self, value):

        interrupt_response_time = value['interrupt_clock_cycle'] * (1/value['clock_frequency'])
        run_isr_time = value['isr_instructions'] * value['instruction_clock_cycle'] * (1/value['clock_frequency'])
        time_spent = round(interrupt_response_time + run_isr_time, 3)

        if time_spent.is_integer():
            time_spent = int(time_spent)

        data_rate = round(((value['data_item_bits'] * value['data_item_numbers'])/time_spent) * 1000)

        return {
            'answer_interrupt_response': str(time_spent),
            'answer_data_rate': str(data_rate)
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

        student_answer['answer_interrupt_response'] = student_answer['answer_interrupt_response'].replace(' ', '').replace('\t', '')
        student_answer['answer_data_rate'] = student_answer['answer_data_rate'].replace(' ', '').replace('\t', '')

        is_valid_interrupt_response, message_type_interrupt_response = self.is_valid_float(student_answer['answer_interrupt_response'])
        is_valid_data_rate, message_type_data_rate = self.is_valid_int(student_answer['answer_data_rate'])

        if not is_valid_interrupt_response:
            if message_type_interrupt_response == 'format':
                self.wrong_format_message = ('Your interrupt response time answer did not have a correct Decimal'
                                             'format. Please try again')
            else:
                self.wrong_format_message = 'The interrupt response time field must be filled in. Please try again'
        elif not is_valid_data_rate:
            if message_type_data_rate == 'format':
                self.wrong_format_message = ('Your data rate answer did not have a correct ' 
                                             'whole number format. You need to round it if it has fraction.' 
                                             'Please try again')
            else:
                self.wrong_format_message = 'The data rate answer field must be filled in. Please try again'

        return is_valid_interrupt_response and is_valid_data_rate

