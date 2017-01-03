SHELL := bash

YOUR_ARM_LD := ~/work/monodroid.c9/monodroid/external/android-sdk-tool/android-ndk/toolchains/arm-linux-androideabi-4.9/prebuilt/darwin-x86_64/bin/arm-linux-androideabi-ld

.PRECIOUS: %.elf %.disasm %.s

all: 3_01/spmtx.disasm

%.disasm: %.elf
	gobjdump -b elf32-littlearm -m armv4t -D $< > $@

%.elf: %.o
	$(YOUR_ARM_LD) -o $@ $<

%.o: %.s
	as --target=arm -mfloat-abi=soft -o $@ $<

%.s: %.sax
	./sax2s.py $<

.PHONY: clean
clean:
	rm -rf 3_01/spmtx.{s,o,elf,disasm}
