My playground to reverse engineer the firmware update file of the Spektrum DX8.

The `.sax` extension indicates their custom file format for describing firmware payload.
It has simple textual format, that are likely instructions for a zero-stage bootloader, let's call it `boot0`.
The file format is likely inspired by [SREC](https://en.wikipedia.org/wiki/SREC_(file_format)).

Commands are separated by `0x1a` and the known one are:

* `#`: Interpret the following string as comment.
* `T`: followed by a string, `\0` terminated. Presumably a debug message printed by `boot0`.
* `:`: ??? not sure yet. One is issued after a text command with "Erasing", and containing some address that happens to be the same where it's going to write. It looks like the first byte after `:` is a command (erasing therefore seems to be `0x10`), but there are also `0xc0`, `0xdf` and `0xef`.
* `SC`: it is followed by an address (four bytes), up to `0x100` bytes of data and a byte of checksum (not clear yet how to compute the checksum). What is weird is, that there is no specifier of how many bytes are to expect. It's like "read until you see `0x1a`".
* `0xd`: followed by a `0x1a` is the end of the `.sax` file.

The address range starts of one of the firmwares I'm looking at (3.01 for DX8), starts at `0x00104000` which is sound with the information from the `AT91SAM7S512` datasheet: The internal flash is mapped to `0x001000000--0x001fffff`.

Executing `strings` on the resulting binary file: https://gist.github.com/lewurm/23bf50595c0274efebc07c3ed3d20e78

```
$ gobjdump -b binary -m armv4t --adjust-vma=0x00104000 --disassembler-options=force-thumb -D 3_01/spmtx.bin
```

## Related Work

* http://www.rc-cam.com/forum/index.php?/topic/2064-hacking-the-i2c-interface-of-spektrum-dx-and-ar/
* http://forum.mikrokopter.de/topic-post242250.html#post242250
* https://github.com/opentx/opentx

## Videos

* internals of DX8: https://www.youtube.com/watch?v=bWobptDQ3FU
