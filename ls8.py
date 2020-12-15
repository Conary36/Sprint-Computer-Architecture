"""Main."""

from cpu import *
import sys

cpu = CPU()

if len(sys.argv) != 2:
    print(f'Error from {sys.argv[0]}: missing filename argument')
    print(f'Usage: python3 {sys.argv[0]} <somefilename>')
    sys.exit(1)
else:
    filename = sys.argv[1]

cpu = CPU()
cpu.load(filename)
cpu.run()

