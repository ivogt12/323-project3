
class Semantics:
    def __init__(self, output_fp):
        self.output_fp = output_fp
        self.symbol_table = {}
        self.next_memory_address = 10000
        self.current_qualifier = None
        
        # Instruction table
        self.instruction_table = {}
        self.next_instruction_address = 1
        
        # Control structures stack
        self.jump_stack = []
        
    def add_to_symbol_table(self, identifier):
        if identifier in self.symbol_table:
            raise ValueError(f"Identifier '{identifier}' already declared")
        self.symbol_table[identifier] = {
            "address": self.next_memory_address,
            "type": self.current_qualifier
        }
        self.next_memory_address += 1
    
    def get_address(self, identifier):
        """Get memory address of identifier"""
        if identifier not in self.symbol_table:
            raise ValueError(f"Identifier '{identifier}' not declared")
        return self.symbol_table[identifier]
    
    def generate_instruction(self, op, operand=None):
        if isinstance(operand, dict) and 'address' in operand:
            operand = operand['address']
        instruction = {
            'address': self.next_instruction_address,
            'op': op,
            'operand': operand
        }
        self.instruction_table[self.next_instruction_address] = instruction
        self.next_instruction_address += 1
        return instruction['address']
    
    def push_jump(self, address):
        """Push jump address to stack for later backpatching"""
        self.jump_stack.append(address)
    
    def back_patch(self, jump_address):
        """Backpatch a jump instruction with the correct address"""
        if not self.jump_stack:
            raise ValueError("Jump stack is empty")
        addr = self.jump_stack.pop()
        self.instruction_table[addr]['operand'] = jump_address

    def print_tables(self):
        print("\nSymbol Table:")
        self.output_fp.write("\nSymbol Table:\n")
        print("Identifier MemoryLocation Type")
        self.output_fp.write("Identifier MemoryLocation Type\n")
        for identifier, data in self.symbol_table.items():
            print(f"{identifier.ljust(11)} {data['address']}        {data['type']}")
            self.output_fp.write(f"{identifier.ljust(11)} {data['address']}        {data['type']}\n")

        print("\nInstruction Table:")
        self.output_fp.write("\nInstruction Table:\n")
        for address, instr in sorted(self.instruction_table.items()):
            op = instr['op']
            operand = str(instr['operand']) if instr['operand'] is not None else ""
            
            print(f"{str(address).ljust(4)} {op.ljust(6)} {operand.rjust(6)}".rstrip())
            self.output_fp.write(f"{str(address).ljust(4)} {op.ljust(6)} {operand.rjust(6)}\n")
        print("\n")
        self.output_fp.flush()
        self.output_fp.close()
        