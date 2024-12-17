import random
from collections import deque

# Instruction Set
class Instruction:
    def __init__(self, opcode, operand1=None, operand2=None):
        self.opcode = opcode  # e.g., "ADD", "SUB", "LOAD", "STORE"
        self.operand1 = operand1
        self.operand2 = operand2

    def __repr__(self):
        return f"{self.opcode} {self.operand1} {self.operand2}"

# Memory Component
class Memory:
    def __init__(self, size):
        self.size = size
        self.data = [0] * size

    def read(self, address):
        return self.data[address]

    def write(self, address, value):
        self.data[address] = value

# Cache Component
class Cache:
    def __init__(self, size, memory):
        self.size = size
        self.memory = memory
        self.cache = {}
        self.access_order = deque()  # For LRU policy

    def read(self, address):
        if address in self.cache:  # Cache hit
            self.access_order.remove(address)
            self.access_order.append(address)
            return self.cache[address]
        else:  # Cache miss
            value = self.memory.read(address)
            self._add_to_cache(address, value)
            return value

    def write(self, address, value):
        if address in self.cache:
            self.access_order.remove(address)
        self._add_to_cache(address, value)
        self.memory.write(address, value)

    def _add_to_cache(self, address, value):
        if len(self.cache) >= self.size:  # Evict the least recently used
            evict_address = self.access_order.popleft()
            del self.cache[evict_address]
        self.cache[address] = value
        self.access_order.append(address)

# CPU Component
class CPU:
    def __init__(self, cache):
        self.cache = cache
        self.registers = [0] * 8  # 8 general-purpose registers

    def execute(self, instruction):
        if instruction.opcode == "LOAD":
            self.registers[instruction.operand1] = self.cache.read(instruction.operand2)
        elif instruction.opcode == "STORE":
            self.cache.write(instruction.operand2, self.registers[instruction.operand1])
        elif instruction.opcode == "ADD":
            self.registers[instruction.operand1] = self.registers[instruction.operand2] + self.registers[instruction.operand1]
        elif instruction.opcode == "SUB":
            self.registers[instruction.operand1] -= self.registers[instruction.operand2]
        elif instruction.opcode == "NOP":
            pass  # No operation
        else:
            raise ValueError(f"Unknown opcode: {instruction.opcode}")

# Simulator Driver
def run_simulator():
    memory = Memory(1024)  # Main memory of 1024 words
    cache = Cache(16, memory)  # Cache with 16 lines
    cpu = CPU(cache)

    # Load some instructions
    program = [
        Instruction("LOAD", 0, 10),  # Load memory[10] into R0
        Instruction("LOAD", 1, 20),  # Load memory[20] into R1
        Instruction("ADD", 0, 1),    # R0 = R0 + R1
        Instruction("STORE", 0, 30), # Store R0 into memory[30]
        Instruction("NOP"),          # No operation
    ]

    # Pre-fill memory with some values
    memory.write(10, 5)
    memory.write(20, 10)

    # Execute program
    for inst in program:
        print(f"Executing: {inst}")
        cpu.execute(inst)
        print(f"Registers: {cpu.registers}")

    # Check memory state
    print(f"Memory[30]: {memory.read(30)}")

# Run the simulation
run_simulator()
