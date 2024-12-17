Plan for CPU Simulator
CPU Core:

Simulates a basic processing unit capable of executing instructions.
Include a simple instruction set (e.g., arithmetic, logic, load/store, and control flow).
Registers to store temporary data.

Cache:

Simulate a small memory for faster access (L1 or L2 cache).
Implement cache replacement policies (e.g., LRU, FIFO).
Handle cache hits and misses.

Memory Bus:

Acts as the interface between the CPU and main memory.
Simulates latency and data transfer.

Main Memory:

A simple large storage for data.
Interacts with the cache via the memory bus.

Instruction Execution Flow:

Fetch, decode, execute cycle.
Memory load/store via cache and memory bus.