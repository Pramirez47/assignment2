import unittest
from disassembler import decode_instruction

class TestInstructionDecoder(unittest.TestCase):
    def test_special_r_type(self):
        self.assertEqual(decode_instruction(0b11111111100000000000000000000000), "PRNL")  # PRNL
        self.assertEqual(decode_instruction(0b11111111101000000000000000000010), "PRNT X2")  # PRNT with Rd=X2
        self.assertEqual(decode_instruction(0b11111111110000000000000000000000), "DUMP")  # DUMP
        self.assertEqual(decode_instruction(0b11111111111000000000000000000000), "HALT")  # HALT

    def test_r_type(self):
        self.assertEqual(decode_instruction(0b10001011000000000000000100000010), "ADD X2, X8, X0")  # ADD with Rd=X2
        self.assertEqual(decode_instruction(0b10001011000000001000100100000110), "ADD X6, X8, X0")  # ADD with Rd=X6, Rn=X8, Rm=X0
        self.assertEqual(decode_instruction(0b11001011000000001000100100001001), "SUB X9, X8, X0")  # SUB with Rd=X9

    def test_d_type(self):
        self.assertEqual(decode_instruction(0b11111000010000000000000000000100), "LDUR X4, [X0, #0]")
        self.assertEqual(decode_instruction(0b11111000000000000000000000000101), "STUR X5, [X0, #0]")

    def test_i_type(self):
        self.assertEqual(decode_instruction(0b10010001000000000000000000000110), "ADDI X6, X0, #0")
        self.assertEqual(decode_instruction(0b10010010000000000000000000000111), "ANDI X7, X0, #0")

    def test_b_type(self):
        self.assertEqual(decode_instruction(0b00010100000000000000000000000000), "B #0")
        self.assertEqual(decode_instruction(0b10010100000000000000000000001000), "BL #8")

    def test_cb_type(self):
        self.assertEqual(decode_instruction(0b10110101000000000000000000001001), "CBNZ X9, #0")
        self.assertEqual(decode_instruction(0b01010100000000000000000000001010), "B.cond #0, condition=GE")

    def test_unknown(self):
        self.assertEqual(decode_instruction(0b11100000000000000000000000000000), "UNKNOWN INSTRUCTION")

if __name__ == "__main__":
    unittest.main()
