import unittest
from disassembler import decode_instruction

class TestInstructionDecoder(unittest.TestCase):
    def test_r_type(self):
        # self.assertEqual(decode_instruction(0b10001011000000000000000100000010), "ADD X2, X2, X0")  # ADD with Rd=X2
        self.assertEqual(decode_instruction(0b10001011000000001000100100000110), "ADD X6, X4, X3")  # ADD with Rd=X6, Rn=X4, Rm=X3
        self.assertEqual(decode_instruction(0b11001011000000001000100100001001), "SUB X9, X4, X3")  # SUB with Rd=X9
        self.assertEqual(decode_instruction(0b10011011000001010100000000001000), "MUL X8, X10, X5")  # MUL with Rd=X8
        self.assertEqual(decode_instruction(0b10101010000000100000000000000010), "ORR X2, X8, X0")  # ORR with Rd=X2
        self.assertEqual(decode_instruction(0b11010011011000110000100000001011), "LSL X11, X4, X3")  # LSL with Rd=X11
        self.assertEqual(decode_instruction(0b11010011010001000001001000001100), "LSR X12, X8, X5")  # LSR with Rd=X12
        self.assertEqual(decode_instruction(0b10001010000000110000000000000011), "AND X3, X12, X0")  # AND with Rd=X3
        self.assertEqual(decode_instruction(0b10101010000001010000000000001101), "ORR X13, X10, X5") # ORR with Rd=X13
        self.assertEqual(decode_instruction(0b11001011000000010000100000001110), "SUB X14, X8, X1")  # SUB with Rd=X14

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
