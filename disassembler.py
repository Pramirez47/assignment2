import sys

def get_register_name(register):
    """
    Returns the appropriate name for a given register number.
    Handles special cases for XZR, SP, and LR.
    """
    if register == 31:
        return "XZR"
    elif register == 28:
        return "SP"
    elif register == 30:
        return "LR"
    return f"X{register}"  # Default case for other registers
# Map of condition codes for B.cond

# Empty at Start
label_map = {}
next_label_number = 1  # Start with Label1




condition_codes = {
    0x0: "EQ",  # Equal
    0x1: "NE",  # Not equal
    0x2: "HS",  # Unsigned higher or same
    0x3: "LO",  # Unsigned lower
    0x4: "MI",  # Minus
    0x5: "PL",  # Plus
    0x6: "VS",  # Overflow
    0x7: "VC",  # No overflow
    0x8: "HI",  # Unsigned higher
    0x9: "LS",  # Unsigned lower or same
    0xA: "GE",  # Signed greater or equal
    0xB: "LT",  # Signed less than
    0xC: "GT",  # Signed greater than
    0xD: "LE",  # Signed less than or equal
}

# Centralized opcode map
opcode_map = {
    # R-Type Opcodes
    0b10001011000: ("R-Type", "ADD"),
    0b10001010000: ("R-Type", "AND"),
    0b11001011000: ("R-Type", "SUB"),
    0b11101011000: ("R-Type", "SUBS"),
    0b10011011000: ("R-Type", "MUL"),
    0b11010011011: ("R-Type", "LSL"),
    0b11010011010: ("R-Type", "LSR"),
    0b10101010000: ("R-Type", "ORR"),

    # D-Type Opcodes
    0b11111000010: ("D-Type", "LDUR"),
    0b11111000000: ("D-Type", "STUR"),

    # I-Type Opcodes
    0b1001000100: ("I-Type", "ADDI"),
    0b1001001000: ("I-Type", "ANDI"),
    0b1101000100: ("I-Type", "SUBI"),
    0b1011001000: ("I-Type", "ORRI"),

    # B-Type Opcodes
    0b000101: ("B-Type", "B"),
    0b100101: ("B-Type", "BL"),


    # CB-Type Opcodes
    0b10110101: ("CB-Type", "CBNZ"),
    0b10110100: ("CB-Type", "CBZ"),
    0b01010100: ("CB-Type", "B.cond"),

    # Extra Opcodes
    0b11111111100: ("R-Type", "PRNL"),  # Prints a blank line
    0b11111111101: ("R-Type", "PRNT"),  # Prints a register's content
    0b11111111110: ("R-Type", "DUMP"),  # Displays registers and memory
    0b11111111111: ("R-Type", "HALT"),  # Halts the program
    0b11010110000: ("R-Type", "BR"),


}


def get_label(address):
    global next_label_number
    if address not in label_map:
        label_map[address] = f"Label{next_label_number}"
        next_label_number += 1
    return label_map[address]



    
# Updated R-Type Decoder
def decode_r_type(instruction, name):
    # Check for special cases first
    if name == "BR":
        Rn = (instruction >> 5) & 0x1F  # Extract Rn (bits 5–9)
        return f"{name} {get_register_name(Rn)}"  # BR uses only Rn

    if name == "PRNL":
        return "PRNL"  # No additional fields
    elif name == "DUMP":
        return "DUMP"  # No additional fields
    elif name == "HALT":
        return "HALT"  # No additional fields
    elif name == "PRNT":
        Rd = instruction & 0x1F  # Extract Rd (bits 0-4)
        return f"PRNT {get_register_name(Rd)}"  # Use Rd for the register to print

    # Default R-Type decoding
    Rm = (instruction >> 16) & 0x1F  # Bits 16-20
    shamt = (instruction >> 10) & 0x3F  # Bits 10-15
    Rn = (instruction >> 5) & 0x1F  # Bits 5-9
    Rd = instruction & 0x1F  # Bits 0-4
    return f"{name} {get_register_name(Rd)}, {get_register_name(Rn)}, {get_register_name(Rm)}"  # Assembly format


# Updated D-Type Decoder
def decode_d_type(instruction, name):
    address = (instruction >> 12) & 0x1FF  # Bits 12-20
    Rn = (instruction >> 5) & 0x1F  # Bits 5-9
    Rt = instruction & 0x1F  # Bits 0-4
    return f"{name} {get_register_name(Rt)}, [{get_register_name(Rn)}, #{address}]"  # Assembly format


# Updated I-Type Decoder
def decode_i_type(instruction, name):
    immediate = (instruction >> 10) & 0xFFF  # Bits 10-21
    Rn = (instruction >> 5) & 0x1F  # Bits 5-9
    Rd = instruction & 0x1F  # Bits 0-4
    return f"{name} {get_register_name(Rd)}, {get_register_name(Rn)}, #{immediate}"  # Assembly format

#  B-Type Decoder
def decode_b_type(instruction, name, current_pc):
    # Extract the 26-bit offset (bits 0-25)
    offset = instruction & 0x3FFFFFF

    # Sign-extend the offset to 32 bits
    if offset & 0x2000000:  # If the sign bit (bit 25) is set
        offset -= 0x4000000  # Subtract 2^26 to handle negative values

    # Calculate the target address (current PC + offset * 4)
    target_address = current_pc + (offset << 2)

    # Get or assign a label for the target address
    label = get_label(target_address)

    return f"{name} {label}"





    
# Updated CB-Type Decoder
def decode_cb_type(instruction, name):
    address = (instruction >> 5) & 0x7FFFF  # Extract 19 bits for address (bits 5-23)
    Rt = instruction & 0x1F  # Extract 5 bits for Rt (bits 0-4)

    if name == "B.cond":  # Handle B.cond instructions
        condition = condition_codes.get(Rt, f"Unknown condition ({Rt})")
        return f"{name} #{address}, condition={condition}"

    return f"{name} {get_register_name(Rt)}, #{address}"  # Handle CBNZ and CBZ
    
def decode_instruction(instruction, current_pc):
    # Step 1: Check R-Type (Opcode in bits 21–31)
    opcode = (instruction >> 21) & 0x7FF  # Extract 11 bits
    if opcode in opcode_map and opcode_map[opcode][0] == "R-Type":
        _, name = opcode_map[opcode]
        return decode_r_type(instruction, name)

    # Step 2: Check D-Type (Opcode in bits 21–31)
    if opcode in opcode_map and opcode_map[opcode][0] == "D-Type":
        _, name = opcode_map[opcode]
        return decode_d_type(instruction, name)

    # Step 3: Check I-Type (Opcode in bits 22–31)
    opcode = (instruction >> 22) & 0x3FF  # Extract 10 bits
    if opcode in opcode_map and opcode_map[opcode][0] == "I-Type":
        _, name = opcode_map[opcode]
        return decode_i_type(instruction, name)

    # Step 4: Check B-Type (Opcode in bits 26–31)
    opcode = (instruction >> 26) & 0x3F  # Extract 6 bits
    if opcode in opcode_map and opcode_map[opcode][0] == "B-Type":
        _, name = opcode_map[opcode]
        return decode_b_type(instruction, name, current_pc)  # Pass current_pc

    # Step 5: Check CB-Type (Opcode in bits 24–31)
    opcode = (instruction >> 24) & 0xFF  # Extract 8 bits
    if opcode in opcode_map and opcode_map[opcode][0] == "CB-Type":
        _, name = opcode_map[opcode]
        return decode_cb_type(instruction, name)

    # If no match is found, return "UNKNOWN INSTRUCTION"
    return "UNKNOWN INSTRUCTION"


    # If no match is found, return "UNKNOWN INSTRUCTION"
    return "UNKNOWN INSTRUCTION"

def decode_file(filename):
    """
    Reads a file and decodes instructions, tracking the program counter.
    """
    try:
        current_pc = 0x0  # Start program counter at 0x0
        with open(filename, "rb") as file:  # Open in binary read mode
            while True:
                # Read 4 bytes (32 bits) at a time
                bytes_read = file.read(4)
                if not bytes_read:  # End of file
                    break

                # Convert 4 bytes into a 32-bit integer in big-endian format
                binary_instruction = int.from_bytes(bytes_read, byteorder="big")

                # Decode the instruction
                decoded_instruction = decode_instruction(binary_instruction, current_pc)
                print(f"{current_pc:08X}: {decoded_instruction}")  # Print address and instruction

                # Increment the program counter by 4 (size of one instruction)
                current_pc += 4
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except ValueError as e:
        print(f"Error: {e}")



def main():
    """
    Main function to handle command-line arguments and execute the disassembler.
    """
    if len(sys.argv) != 2:  # Ensure one argument is passed
        print("Usage: python disassembler.py <filename>")
        return

    filename = sys.argv[1]  # Get the filename from command-line arguments
    decode_file(filename)  # Decode the instructions in the file


if __name__ == "__main__":
    main()  # Run the main function