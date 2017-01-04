SHELL := bash

# define the path to your arm toolchain, android ndk works fine for me.
YOUR_ARM_PREFIX ?= ~/work/monodroid.c9/monodroid/external/android-sdk-tool/android-ndk/toolchains/arm-linux-androideabi-4.9/prebuilt/darwin-x86_64/bin/arm-linux-androideabi-

CC := $(YOUR_ARM_PREFIX)gcc
LD := $(YOUR_ARM_PREFIX)ld

.PRECIOUS: %.elf %.disasm %.s %.o

all: 3_01/spmtx.disasm

%.disasm: %.elf
	gobjdump -b elf32-littlearm -m armv4t -D $< > $@

%.elf: %.o
	$(LD) -T firmware.lds -o $@ $<

%.o: %.s
	$(CC) -mtune=arm7tdmi -c -o $@ $<

%.s: %.sax
	./sax2s.py $<

.PHONY: clean
clean:
	rm -rf 3_01/spmtx.{s,o,elf,disasm}
