OUTPUT_FORMAT("elf32-littlearm")
OUTPUT_ARCH(arm:common)

SECTIONS {
    .dx8hacks 0x00104000:
    {
          *.o(.start)
    }
}
