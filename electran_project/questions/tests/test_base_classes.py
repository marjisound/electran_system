from django.test import TestCase
from questions.custom.question_classes import base_classes


class FixedLength(TestCase):

    def setUp(self):
        self.sub_signed_negative_positive = {'val1': 4294906129, 'val2': 536870911}
        self.sub_signed_negative_positive2 = {'val1': 4022364619, 'val2': 81383}
        self.sub_signed_negative_positive3 = {'val1': 4022364619, 'val2': 2004221952}
        # 0x77760000 - 0xefc069cb
        self.add_signed_positive_negative = {'val1': 2004221952, 'val2': 4022364619}
        self.add_signed_negative_negative = {'val1': 4294906129, 'val2': 27083}

    def test_sub_rtype(self):
        """
        This test is for signed subtraction
        """
        question = base_classes.MipsInstructionsBase()
        expected = question.sub_rtype(self.sub_signed_negative_positive)

        correct_result = ('dfff1112', False)
        self.assertEqual(correct_result, expected)

        expected = question.sub_rtype(self.sub_signed_negative_positive2)
        correct_result = ('efbf2be4', False)
        self.assertEqual(correct_result, expected)

        expected = question.sub_rtype(self.sub_signed_negative_positive3)
        correct_result = ('784a69cb',  True)
        self.assertEqual(correct_result, expected)

    def test_subu_rtype(self):
        """
        This test is for signed subtraction
        """
        question = base_classes.MipsInstructionsBase()
        expected = question.subu_rtype(self.sub_signed_negative_positive)

        correct_result = ('dfff1112', None)
        self.assertEqual(correct_result, expected)

        expected = question.subu_rtype(self.sub_signed_negative_positive2)
        correct_result = ('efbf2be4', None)
        self.assertEqual(correct_result, expected)

        expected = question.subu_rtype(self.sub_signed_negative_positive3)
        correct_result = ('784a69cb',  None)
        self.assertEqual(correct_result, expected)

    def test_add_rtype(self):
        """
        This test is for signed subtraction
        """
        question = base_classes.MipsInstructionsBase()
        expected = question.add_rtype(self.add_signed_positive_negative)

        correct_result = ('673669cb', False)
        self.assertEqual(correct_result, expected)

        expected = question.add_rtype(self.add_signed_negative_negative)
        correct_result = ('ffff7adc', False)
        self.assertEqual(correct_result, expected)

    def test_addu_rtype(self):
        """
        This test is for signed subtraction
        """
        question = base_classes.MipsInstructionsBase()
        expected = question.addu_rtype(self.add_signed_positive_negative)

        correct_result = ('673669cb', None)
        self.assertEqual(correct_result, expected)

        expected = question.addu_rtype(self.add_signed_negative_negative)
        correct_result = ('ffff7adc', None)
        self.assertEqual(correct_result, expected)

    def test_addi_itype(self):
        """
        This test is for signed extended immediate + rs (signed addition)
        """
        value = {'val1': 4294906129, 'val2': 46000}
        question = base_classes.MipsInstructionsBase()
        expected = question.addi_itype(value)

        correct_result = ('fffec4c1', False)
        self.assertEqual(correct_result, expected)

        value = {'val1': 2190429777, 'val2': 32768}
        expected = question.addi_itype(value)
        correct_result = ('828ece51', False)
        self.assertEqual(correct_result, expected)

        value = {'val1': 22016, 'val2': 43818}
        expected = question.addi_itype(value)
        correct_result = ('0000012a', False)
        self.assertEqual(correct_result, expected)

        value = {'val1': 3072, 'val2': 8569}
        expected = question.addi_itype(value)
        correct_result = ('00002d79', False)
        self.assertEqual(correct_result, expected)

    def test_addiu_itype(self):
        """
        This test is for signed extended immediate + rs (signed addition)
        """
        value = {'val1': 4294906129, 'val2': 46000}
        question = base_classes.MipsInstructionsBase()
        expected = question.addi_itype(value)

        correct_result = ('fffec4c1', False)
        self.assertEqual(correct_result, expected)

    def test_slti_itype(self):
        """
        This test is for signed extended immediate + rs (signed addition)
        """
        value = {'val1': 2818572387, 'val2': 39269}
        question = base_classes.MipsInstructionsBase()
        expected = question.slti_itype(value)

        correct_result = ('00000001', None)
        self.assertEqual(correct_result, expected)

    def test_ori_itype(self):
        """
        This test is for signed extended immediate + rs (signed addition)
        """
        value = {'val1': 3850272856, 'val2': 3}
        question = base_classes.MipsInstructionsBase()
        expected = question.ori_itype(value)

        correct_result = ('e57e805b', None)
        self.assertEqual(correct_result, expected)

    def test_andi_itype(self):
        """
        This test is for signed extended immediate + rs (signed addition)
        """
        value = {'val1': 528362263, 'val2': 1008}
        question = base_classes.MipsInstructionsBase()
        expected = question.andi_itype(value)

        correct_result = ('00000310', None)
        self.assertEqual(correct_result, expected)






