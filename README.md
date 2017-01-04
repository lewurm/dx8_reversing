My playground to reverse engineer the firmware update file of the Spektrum DX8.

The `.sax` extension indicates their custom file format for describing firmware payload.
It has simple textual format, that are likely instructions for a zero-stage bootloader, let's call it `boot0`.
The file format is likely inspired by [SREC](https://en.wikipedia.org/wiki/SREC_(file_format)).

Commands are separated by `0x1a` and the known one are:

* `#`: Interpret the following string as comment.
* `T`: followed by a string, `\0` terminated. Presumably a debug message printed by `boot0`.
* `:`: ??? not sure yet. One is issued after a text command with "Erasing", and containing some address that happens to be the same where it's going to write. It looks like the first byte after `:` is a command (erasing therefore seems to be `0x10`), but there are also `0xc0`, `0xdf` and `0xef`.
* `SC`: it is followed by an address (four bytes), one byte describing the length in words (4 bytes), and up to `0x100` bytes of data. There is no checksum.
* `0xd`: followed by a `0x1a` is the end of the `.sax` file.

The address range starts of one of the firmwares I'm looking at (3.01 for DX8), starts at `0x00104000` which is sound with the information from the `AT91SAM7S512` datasheet: The internal flash is mapped to `0x001000000--0x001fffff`.

## useful commands

```
$ make
$ # get a list of strings with correct offsets in ELF
$ rabin2 -zz 3_01/spmtx.elf
```

Output: https://gist.github.com/b52f0e3cf4c363f087d4f8ed34f04aed

Interesting stuff starts at `0x00146748`.

## Road to `boot0`

In order to fully understand the custom file format, we need to understand how `boot0` works.
Presumably (or hopefully), the pages on the flash storage containing `boot0` are locked in the sense of that the cannot be overwritten (that would be a good thing).
Assuming that, it would be "safe" to temper with a `.sax` file and if something goes wrong, we could just fall back to the official firmware file and restore the firmware on the device.
However, that's just a dangerous assumption: What if the pages of `boot0` aren't locked and thus we may end up bricking the device?

Thus, I propose the following attack plan:
* reverse the firmware, identify the part where it reads configurations from a SD-card.
* find buffer overflow vuln.
* exploit it, dump flash content to SD-card (assuming that those pages are readable in firmware mode).
* have `boot0`.

With that we can safely analyze `boot0` and decide if tempering with the `.sax` file is safe enough.

## Related Work

* http://www.rc-cam.com/forum/index.php?/topic/2064-hacking-the-i2c-interface-of-spektrum-dx-and-ar/
* http://forum.mikrokopter.de/topic-post242250.html#post242250
* https://github.com/opentx/opentx

## Videos

* internals of DX8: https://www.youtube.com/watch?v=bWobptDQ3FU

