from questions.custom.question_classes.base_classes import BinaryHexBase, MipsInstructionsBase
import random
import os
import codecs


class Question(MipsInstructionsBase, BinaryHexBase):
    ANSWER_TYPE = 'multiple'
    display_correct = []

    def generate_user_random_display(self, value):
        return value

    def generate_random(self):
        shift = random.randint(1, 31)
        rt = random.randint(1, 31)
        rd = random.randint(1, 31)

        instruction_type = random.choice(self.RTYPE_GROUPS['no_rs'])

        register_dict = self.random_registers()

        memory_dict = self.random_memories()

        pc = '0x' + '{:0>8}'.format(codecs.encode(os.urandom(4), 'hex').decode())

        return {'shift': shift, 'rt': rt, 'rd': rd, 'pc': pc,
                'instruction_type': instruction_type, 'instruction_format': 'R',
                'registers': register_dict, 'memory_locations': memory_dict}

    def expected_answer(self, value):
        func_values = {
            'val1': int(value['registers'][str(value['rt'])], 16),
            'shift': value['shift']
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

    def test_answer(self, student_answer, correct_answer):
        new_student_list = student_answer
        new_correct_list = correct_answer

        new_correct_list['answer_register_value'] = new_correct_list['answer_register_value'].lower()
        register_value = student_answer['answer_register_value'].replace(' ', '')
        register_value = self.delete_hex_identifier(register_value.lower())
        new_student_list['answer_register_value'] = '{:0>8}'.format(register_value)

        new_student_list['answer_register_num'] = int(new_student_list['answer_register_num'])

        pc_value = student_answer['answer_pc_value'].replace(' ', '')
        pc_value = self.delete_hex_identifier(pc_value.lower())
        new_student_list['answer_pc_value'] = '{:0>8}'.format(pc_value)

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




