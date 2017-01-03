SHELL := bash

.PRECIOUS: %.elf %.disasm %.s

all: 3_01/spmtx.disasm

%.disasm: %.elf
	gobjdump -b elf32-littlearm -m armv4t -D $< > $@

%.elf: %.s
	as --target=arm -mfloat-abi=soft -o $@ $<

%.s: %.sax
	./sax2s.py $<

.PHONY: clean
clean:
	rm -rf 3_01/spmtx.{s,elf,disasm}
