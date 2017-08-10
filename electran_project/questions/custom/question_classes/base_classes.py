import random


class QuestionBase:
    """Common base class for all questions"""
    wrong_answer_message = 'Wrong Answer'
    correct_answer_message = 'Correct Answer'
    wrong_format_message = 'Your answer did not have a correct format. Please try again'

    def generate_random(self):
        return None

    def expected_answer(self):
        return None

    def test_answer(self):
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
        else:
            return value

    @staticmethod
    def delete_hex_identifier(value):
        if value.startswith('0x') or value.startswith('0X'):
            return value[2:]
        else:
            return value

    @staticmethod
    def delete_octal_identifier(value):
        if value.startswith('0o') or value.startswith('0O'):
            return value[2:]
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
    def spacing_binary_numbers(value, bit_num):
        formatted_value = value.replace(' ', '')
        while len(formatted_value) < bit_num:
            formatted_value = '0' + formatted_value
        return ' '.join([value[i:i + 4] for i in range(0, len(value), 4)])


class MipsInstructionsBase(QuestionBase):

    RTYPE_OP = 0
    RTYPE_SHAMT = 0

    RTYPE_VALUES = {
        'sll': 0x00,
        'srl': 0x02,
        'jr': 0x08,
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
