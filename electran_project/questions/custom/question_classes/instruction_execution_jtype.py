from questions.custom.question_classes.base_classes import BinaryHexBase, MipsInstructionsBase
import random
import os
import codecs


class Question(MipsInstructionsBase, BinaryHexBase):
    ANSWER_TYPE = 'multiple'

    def __init__(self):
        self.display_correct = None

    def generate_user_random_display(self, value):
        new_value = value.copy()
        new_value['immediate'] = hex(value['immediate'])
        return new_value

    def generate_random(self):
        immediate = random.randrange(67108863)

        instruction_type = random.choice(['j', 'jal'])

        register_dict = self.random_registers()

        memory_dict = self.random_memories()

        pc = '0x' + '{:0>8}'.format(codecs.encode(os.urandom(4), 'hex').decode())

        return {'immediate': immediate, 'pc': pc,
                'instruction_type': instruction_type, 'instruction_format': 'J',
                'registers': register_dict, 'memory_locations': memory_dict}

    def expected_answer(self, value):

        func_values = {
            'immediate': value['immediate'],
            'pc': value['pc'][2:]
        }

        calculated, overflow = MipsInstructionsBase.JTYPE_CALCULATIONS[value['instruction_type']](func_values)

        expected = {
            'answer_register': 'unchanged',
            'answer_register_num': None,
            'answer_register_value': None,
            'answer_pc': 'written',
            'answer_pc_value': calculated,
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
            'answer_overflow': overflow
        }

        if value['instruction_type'] == 'jal':
            expected['answer_register'] = 'written'
            expected['answer_register_num'] = str(31)
            expected['answer_register_value'] = value['pc']

        return expected

    def expected_answer_display_format(self, value):
        return value

    def test_answer(self, student_answer, correct_answer):

        new_student_list = student_answer.copy()

        pc_value = student_answer['answer_pc_value'].replace(' ', '')
        pc_value = self.delete_hex_identifier(pc_value.lower())
        new_student_list['answer_pc_value'] = '{:0>8}'.format(pc_value)

        if correct_answer['answer_register'] == 'written':
            register_value = self.delete_hex_identifier(student_answer['answer_register_value'].replace(' ', '').lower())
            new_student_list['answer_register_value'] = '{:0>8}'.format(register_value)

        for key, value in new_student_list.items():
            if value == 'None' or value == '':
                new_student_list[key] = None

        # convert overflow value to boolean
        if new_student_list['answer_overflow'] == '1':
            new_student_list['answer_overflow'] = True
        elif new_student_list['answer_overflow'] == '0':
            new_student_list['answer_overflow'] = False

        diff_list = self.compare_dictionaries(new_student_list, correct_answer)

        self.display_correct = diff_list

        if len(diff_list) == 0:

            return True
        else:
            return False

    def is_valid(self, answer):
        return True




