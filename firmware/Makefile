SHELL := bash

# define the path to your arm toolchain
YOUR_ARM_PREFIX ?= /Applications/ArmGNUToolchain/13.3.rel1/arm-none-eabi/bin/arm-none-eabi-

CC := $(YOUR_ARM_PREFIX)gcc
LD := $(YOUR_ARM_PREFIX)ld
OBJDUMP := $(YOUR_ARM_PREFIX)objdump

.PRECIOUS: %.elf %.disasm %.disasm_thumb %.s %.o

all: 3_01/spmtx.disasm 3_01/spmtx.disasm_thumb

%.disasm: %.elf
	$(OBJDUMP) -b elf32-littlearm -m armv4t -D $< > $@

%.disasm_thumb: %.elf
	$(OBJDUMP) -b elf32-littlearm -m armv4t -Mforce-thumb -D $< > $@

%.elf: %.o
	$(LD) -T firmware.lds -o $@ $<

%.o: %.s
	$(CC) -mtune=arm7tdmi -c -o $@ $<

%.s: %.sax
	python3 ./sax2s.py $<

.PHONY: clean
clean:
	rm -rf 3_01/spmtx.{s,o,elf,disasm,disasm_thumb}
