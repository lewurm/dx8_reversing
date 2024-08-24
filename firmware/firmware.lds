OUTPUT_FORMAT("elf32-littlearm")

SECTIONS {
    .dx8hacks 0x00104000:
    {
          *.o(.start)
    }
}
