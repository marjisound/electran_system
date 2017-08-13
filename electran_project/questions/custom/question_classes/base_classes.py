import random


class QuestionBase:
    """Common base class for all questions"""
    wrong_answer_message = 'Wrong Answer'
    correct_answer_message = 'Correct Answer'
    wrong_format_message = 'Your answer did not have a correct format. Please try again'

    def generate_random(self):
        return None

    def expected_answer(self, value):
        return None

    def test_answer(self, student_answer, correct_answer):
        return False

    def expected_answer_display_format(self, value):
        return value

    def generate_user_random_display(self, value):
        return value

    @staticmethod
    def remove_list_from_list(parent_list, removing_list):
        for item in removing_list:
            if item in parent_list:
                parent_list.remove(item)


class BinaryHexBase(QuestionBase):
    """Common base class for all binary/hex questions"""

    POWER_DICT = {
        'K': 10,
        'M': 20,
        'G': 30
    }

    @staticmethod
    def delete_binary_identifier(value):
        if value.startswith('0b') or value.startswith('0B'):
            return value[2:]
        elif value.startswith('-0b') or value.startswith('-0B'):
            formatted_value = value[3:]
            return '-' + formatted_value
        else:
            return value

    @staticmethod
    def delete_hex_identifier(value):
        if value.startswith('0x') or value.startswith('0X'):
            return value[2:]
        elif value.startswith('-0x') or value.startswith('-0X'):
            formatted_value = value[3:]
            return '-' + formatted_value
        else:
            return value

    @staticmethod
    def delete_octal_identifier(value):
        if value.startswith('0o') or value.startswith('0O'):
            return value[2:]
        elif value.startswith('-0o') or value.startswith('-0O'):
            formatted_value = value[3:]
            return '-' + formatted_value
        else:
            return value

    @staticmethod
    def hex_to_binary(hex_num):
        return bin(int(hex_num, 16))

    @staticmethod
    def binary_to_hex(binary_num):
        return hex(int(binary_num, 2))

    def is_valid_hex(self, hex_num):
        if not hex_num or type(hex_num) != str:
            self.wrong_format_message = 'The answer field must be filled in. Please try again'
            return False, 'field'
        else:
            try:
                hex_num = hex_num.replace(' ', '')
                int(hex_num, 16)
            except ValueError:
                self.wrong_format_message = 'Your answer did not have a correct binary format. Please try again'
                return False, 'format'
            else:
                return True, 'format'

    def is_valid_binary(self, binary_num):
        if not binary_num or type(binary_num) != str:
            self.wrong_format_message = 'The answer field must be filled in. Please try again'
            return False, 'field'
        else:
            try:
                binary_num = binary_num.replace(' ', '')
                int(binary_num, 2)
            except ValueError:
                self.wrong_format_message = 'Your answer did not have a correct binary format. Please try again'
                return False, 'format'
            else:
                return True, 'format'

    def is_valid_oct(self, octal_num):
        if not octal_num or type(octal_num) != str:
            self.wrong_format_message = 'The answer field must be filled in. Please try again'
            return False, 'field'
        else:
            try:
                binary_num = octal_num.replace(' ', '')
                int(binary_num, 8)
            except ValueError:
                self.wrong_format_message = 'Your answer did not have a correct octal format. Please try again'
                return False, 'format'
            else:
                return True, 'format'

    @staticmethod
    def spacing_binary_numbers(value):
        modulo_value = len(value) % 4
        separate_value = value[:modulo_value]
        rest_of_value = value[modulo_value:]
        result = ' '.join([rest_of_value[i:i + 4] for i in range(0, len(rest_of_value), 4)])
        if separate_value:
            result = separate_value + ' ' + result
        return result

    @staticmethod
    def make_specific_number_of_bits(value, bit_length):
        result = value
        overflow = False
        if len(value) > bit_length:
            extra = len(value) - bit_length
            result = value[extra:]
            overflow = True
        elif len(value) < 8:
            format_str = '{:0>' + str(bit_length) + '}'
            result = format_str.format(value)
        return result, overflow


class MipsInstructionsBase(QuestionBase):

    RTYPE_OP = 0
    RTYPE_SHAMT = 0

    RTYPE_VALUES = {
        'add': 0x20,
        'addu': 0x21,
        'sub': 0x22,
        'subu': 0x23,
        'and': 0x24,
        'or': 0x25,
        'xor': 0x26,
        'nor': 0x27,
        'slt': 0x2a,
        'sltu': 0x2b
    }

    RTYPE_SHIFT_VALUES = {
        'sll': 0x00,
        'srl': 0x02,
        'sra': 0x03,
        'jr': 0x08,
    }

    ITYPE_VALUES = {
        'addi': 0x8,
        'addiu': 0x9,
        'andi': 0xc,
        'beq': 0x4,
        'bne': 0x5,
        'lbu': 0x24,
        'lhu': 0x25,
        'll': 0x30,
        'lui': 0xf,
        'lw': 0x23,
        'ori': 0xd,
        'slti': 0xa,
        'sltiu': 0xb,
        'sb': 0x28,
        'sc': 0x38,
        'sh': 0x29,
        'sw': 0x2b
    }

    JTYPE_VALUES = {
        'j': 0x2,
        'jal': 0x3
    }
    MIPS_INS_TYPES = {'R': RTYPE_VALUES, 'I': ITYPE_VALUES, 'J': JTYPE_VALUES}

    MEMORY_LOCATION_STARTING_POINT = 268435456  # this is 0x10000000

    @staticmethod
    def add_rtype(value):
        return value['val1'] + value['val2']

    @staticmethod
    def addu_rtype(value):
        result = value['val1'] + value['val2']
        return result

    @staticmethod
    def sub_rtype(value):
        result = value['val1'] - value['val2']
        return result

    @staticmethod
    def subu_rtype(value):
        result = value['val1'] - value['val2']
        return result

    @staticmethod
    def and_rtype(value):
        result = value['val1'] & value['val2']
        return result

    @staticmethod
    def or_rtype(value):
        result = value['val1'] | value['val2']
        return result

    @staticmethod
    def xor_rtype(value):
        result = value['val1'] ^ value['val2']
        return result

    @staticmethod
    def nor_rtype(value):
        result = ~ (value['val1'] | value['val2'])
        return result

    @staticmethod
    def slt_rtype(value):
        result = 1 if value['val1'] < value['val2'] else 0
        return result

    @staticmethod
    def sltu_rtype(value):
        result = 1 if value['val1'] < value['val2'] else 0
        return result

    RTYPE_CALCULATIONS = {
        'add': add_rtype,
        'addu': addu_rtype,
        'sub': 0x22,
        'subu': 0x23,
        'and': 0x24,
        'or': 0x25,
        'xor': 0x26,
        'nor': 0x27,
        'slt': 0x2a,
        'sltu': 0x2b
    }




    REGISTER_VALUES = {
        '0': 0x00000000,
        '1': 0x00f70000,
        '2': 0x0299cc4a,
        '3': 0x0000d700,
        '4': 0x000007f0,
        '5': 0x05086c4c,
        '6': 0x0000da00,
        '7': 0x0000c722,
        '8': 0xef000088,
        '9': 0x0000aa00,
        '10': 0x00670000,
        '11': 0x00000001,
        '12': 0x00004700,
        '13': 0x006d0000,
        '14': 0x0600009e,
        '15': 0x00000b00,
        '16': 0x001a0000,
        '17': 0x3e0000e4,
        '18': 0x00006700,
        '19': 0x00010000,
        '20': 0xf600004b,
        '21': 0x0000e400,
        '22': 0x00d70000,
        '23': 0x0001487b,
        '24': 0x00009f00,
        '25': 0x00ea0000,
        '26': 0x500000c5,
        '27': 0x39100000,
        '28': 0x00890000,
        '29': 0x160000f6,
        '30': 0x00000f00,
        '31': 0x00e90000
    }

    PC_VALUE = 113983136


