from django.test import TestCase, SimpleTestCase
from questions.custom.question_classes import (instruction_execution_rtype_no_shift,
                                               instruction_decoding_rtype,
                                               instruction_encoding_rtype,
                                               instruction_execution_rtype_no_rs,
                                               instruction_execution_rtype_jump)


class InstructionExecution(TestCase):

    def test_instruction_execution_rtype_no_shift(self):
        """
        Test if instruction_execution_rtype_no_shift question
         calculates the result correctly
        :return:
        """
        question = instruction_execution_rtype_no_shift.Question()

        registers = question.random_registers()

        registers['2'] = '524315b8'
        registers['1'] = '00846c23'

        question_params = {'rs': 2, 'rt': 1, 'rd': 11, 'pc': '148e1452',
                           'instruction_type': 'sltu', 'instruction_format': 'R',
                           'registers': registers,
                           'memory_locations': question.random_memories()}

        question_answer = question.expected_answer(question_params)

        expected = {
            'answer_register': 'written',
            'answer_register_num': 11,
            'answer_register_value': '00000000',
            'answer_pc': 'written',
            'answer_pc_value': '148e1456',
            'answer_memory_0': 'unchanged',
            'answer_memory_0_address': None,
            'answer_memory_0_value': None,
            'answer_memory_1': 'unchanged',
            'answer_memory_1_address': None,
            'answer_memory_1_value': None,
            'answer_memory_2': 'unchanged',
            'answer_memory_2_address': None,
            'answer_memory_2_value': None,
            'answer_memory_3': 'unchanged',
            'answer_memory_3_address': None,
            'answer_memory_3_value': None,
            'answer_overflow': None
        }

        self.assertEqual(question_answer, expected)

    def test_instruction_execution_rtype_no_rs(self):
        """
        Test if instruction_execution_rtype_no_rs question
         calculates the result correctly
        :return:
        """
        question = instruction_execution_rtype_no_rs.Question()

        register_dict = question.random_registers()
        register_dict['26'] = '00001234'

        memory_dict = question.random_memories()

        question_params = {'shift': 11, 'rt': 26, 'rd': 3, 'pc': '81111114',
                           'instruction_type': 'sll', 'instruction_format': 'R',
                           'registers': register_dict, 'memory_locations': memory_dict}

        question_answer = question.expected_answer(question_params)

        expected = {
            'answer_register': 'written',
            'answer_register_num': 3,
            'answer_register_value': '0091a000',
            'answer_pc': 'written',
            'answer_pc_value': '81111118',
            'answer_memory_0': 'unchanged',
            'answer_memory_0_address': None,
            'answer_memory_0_value': None,
            'answer_memory_1': 'unchanged',
            'answer_memory_1_address': None,
            'answer_memory_1_value': None,
            'answer_memory_2': 'unchanged',
            'answer_memory_2_address': None,
            'answer_memory_2_value': None,
            'answer_memory_3': 'unchanged',
            'answer_memory_3_address': None,
            'answer_memory_3_value': None,
            'answer_overflow': None
        }

        self.assertEqual(question_answer, expected)

    def test_instruction_execution_rtype_jump(self):
        """
        Test if instruction_execution_rtype_jump question
         calculates the result correctly
        :return:
        """
        pass
        # question = instruction_execution_rtype_jump.Question()
        #
        # question_params = {'rs': rs, 'rd': rd, 'pc': pc,
        #                     'instruction_type': instruction_type, 'instruction_format': 'R',
        #                     'registers': register_dict, 'memory_locations': memory_dict}


class InstructionEncodingDecoding(SimpleTestCase):

    def test_instruction_decoding_rtype(self):
        """
        Test the instruction_decoding_rtype question to return the correct display
        format to user
        & test if it calculates the result correctly
        :return:
        """
        question = instruction_decoding_rtype.Question()

        question_params = {'rs': 0, 'rt': 15, 'rd': 8, 'shift': 29,
                           'instruction_type': 'srl', 'instruction_format': 'R'}

        # test 1
        display_question = question.generate_user_random_display(question_params)
        self.assertEqual(display_question, '000000 00000 01111 01000 11101 000010')
        # test2
        question_answer = question.expected_answer(question_params)
        self.assertEqual(question_answer, 'srl $8, $15, 0x1d')

        # test3
        question_params = {'rs': 9, 'rt': 22, 'rd': 28, 'shift': 0,
                           'instruction_type': 'xor', 'instruction_format': 'R'}
        question_answer = question.expected_answer(question_params)
        self.assertEqual(question_answer, 'xor $28, $9, $22')

    def test_instruction_encoding_rtype(self):
        """
        Test the instruction_encoding_rtype question to return the correct display
        format to user
        & test if it calculates the result correctly
        :return:
        """
        question = instruction_encoding_rtype.Question()

        question_params = {'rs': 9, 'rt': 22, 'rd': 28, 'shift': 0,
                           'instruction_type': 'xor', 'instruction_format': 'R'}

        # test 1
        display_question = question.generate_user_random_display(question_params)
        self.assertEqual(display_question['random_value'], 'xor $28, $9, $22')





