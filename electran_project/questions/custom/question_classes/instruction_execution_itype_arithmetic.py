from questions.custom.question_classes.base_classes import BinaryHexBase, MipsInstructionsBase
import random
import os
import codecs


class Question(MipsInstructionsBase, BinaryHexBase):
    ANSWER_TYPE = 'multiple'

    def generate_user_random_display(self, value):
        new_value = value
        new_value['immediate'] = hex(value['immediate'])
        return new_value

    def generate_random(self):
        rs = random.randint(1, 31)
        rt = random.randint(1, 31)
        immediate = random.randrange(65535)

        instruction_type = random.choice(self.RTYPE_GROUPS['no_shift'])

        register_dict = self.random_registers()

        memory_dict = self.random_memories()

        pc = '0x' + '{:0>8}'.format(codecs.encode(os.urandom(4), 'hex').decode())

        return {'rs': rs, 'rt': rt, 'immediate': immediate, 'pc': pc,
                'instruction_type': instruction_type, 'instruction_format': 'R',
                'registers': register_dict, 'memory_locations': memory_dict}

    def expected_answer(self, value):

        func_values = {
            'val1': value['immediate'],
            'val2': int(value['registers'][str(value['rs'])], 16)
        }

        calculated, overflow = MipsInstructionsBase.RTYPE_CALCULATIONS[value['instruction_type']](func_values)

        expected = {
            'answer_register': 'written',
            'answer_register_num': value['rd'],
            'answer_register_value': calculated,
            'answer_pc': 'written',
            'answer_pc_value': '{:0>8}'.format(hex(int(value['pc'], 16) + 4)[2:]),
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

        return expected

    def expected_answer_display_format(self, value):
        return value

    def test_answer(self, student_answer, correct_answer):
        register_value = self.delete_hex_identifier(student_answer['answer_register_value'].lower())
        pc_value = self.delete_hex_identifier(student_answer['answer_pc_value'].lower())
        for key, value in student_answer.items():
            if value == 'None' or value == '':
                student_answer[key] = None

        # convert overflow value to boolean
        if student_answer['answer_overflow'] == '1':
            student_answer['answer_overflow'] = True
        elif student_answer['answer_overflow'] == '0':
            student_answer['answer_overflow'] = False

        if (student_answer['answer_register'].lower() == correct_answer['answer_register'].lower() and
                    int(student_answer['answer_register_num']) == correct_answer['answer_register_num'] and
                    '{:0>8}'.format(register_value) == correct_answer['answer_register_value'].lower() and
                    student_answer['answer_pc'] == correct_answer['answer_pc'] and
                    '{:0>8}'.format(pc_value) == correct_answer['answer_pc_value'] and
                    student_answer['answer_overflow'] == correct_answer['answer_overflow'] and
                    student_answer['answer_memory_0'] == correct_answer['answer_memory_0'] and
                    student_answer['answer_memory_0_address'] == correct_answer['answer_memory_0_address'] and
                    student_answer['answer_memory_0_value'] == correct_answer['answer_memory_0_value'] and
                    student_answer['answer_memory_1'] == correct_answer['answer_memory_1'] and
                    student_answer['answer_memory_1_address'] == correct_answer['answer_memory_1_address'] and
                    student_answer['answer_memory_1_value'] == correct_answer['answer_memory_1_value'] and
                    student_answer['answer_memory_2'] == correct_answer['answer_memory_2'] and
                    student_answer['answer_memory_2_address'] == correct_answer['answer_memory_2_address'] and
                    student_answer['answer_memory_2_value'] == correct_answer['answer_memory_2_value'] and
                    student_answer['answer_memory_3'] == correct_answer['answer_memory_3'] and
                    student_answer['answer_memory_3_address'] == correct_answer['answer_memory_3_address'] and
                    student_answer['answer_memory_3_value'] == correct_answer['answer_memory_3_value']):

            return True
        else:
            return False

    def is_valid(self, answer):
        return True




