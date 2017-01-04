#!/usr/local/bin/python2

import sys, struct

with open(sys.argv[1], "r") as fd:
    data = fd.read()

out_file = open(sys.argv[1].replace(".sax", ".s"), "wb")

# input is a string consisting of two chars, representing a byte in hex
def out_byte(byte_string):
    assert (len(byte_string) == 2)
    int(byte_string, 16)
    out_file.write(".byte 0x" + byte_string + "\n")

def out_word(byte_string):
    assert (len(byte_string) == 8)
    out_byte(byte_string[0:2])
    out_byte(byte_string[2:4])
    out_byte(byte_string[4:6])
    out_byte(byte_string[6:8])

data_length = len(data)
first = True

print "[++] input file %s is %d bytes long" % (sys.argv[1], data_length)

fake_newlines = 0
i = 0
payload_length = 0
reached_end = False

while i < data_length:
    if ord(data[i]) == 0x1a:
        fake_newlines += 1
        i += 1
        continue
    elif ord(data[i]) == 0xd and ord(data[i+1]) == 0x1a:
        # end of sax file, we're done here
        assert (i == (data_length - 2))
        reached_end = True
        break
    elif data[i] == ":":
        i += 1
        count = 0
        message = "[++] ??? "
        while ord(data[i]) != 0x1a:
            # out_byte(data[i:i+2])
            # out_byte(data[i+2:i+4])
            if count > 0 and (count % 0x10) == 0:
                message += "\n         0x%s " % data[i:i+4]
            else:
                message += "0x%s " % data[i:i+4]
            i += 4
            count += 4
        print message
        print "[++] breaking ??? at index %d/%d" % (count,i)
        continue
    elif data[i:i+2] == "SC":
        i += 2
        addr = data[i:i+8]
        i += 8
        chunk_length = int(data[i:i+2], 16) * 4
        i += 2
        assert chunk_length <= 0x100, "specified length 0x%x" % chunk_length

        if first:
            out_file.write(".section .start,\"ax\"\n")
            out_file.write("_main:\n")
            first = False

        print "[++] writing 0x%x bytes at addr 0x%s " % (chunk_length, addr)
        real_length = 0
        chunk = ""
        while real_length < (chunk_length * 2):
            assert ord(data[i]) != 0x1a, "invalid encoding"
            out_word(data[i:i+8])
            i += 8
            real_length += 8
        print "[++] got %d / 0x%x bytes of data after addr (specified %d / 0x%x)" % (real_length/2, real_length/2, chunk_length, chunk_length)
        payload_length += chunk_length
        i += 2
        continue
    elif data[i] == "T" or data[i] == "#":
        is_comment = data[i] == "#"
        i += 1
        message = ""
        while ord(data[i]) != 0x1a:
            if ord(data[i]) > 0x00:
                message += data[i]
            i += 1
        print "[++] %s: %s" % ("Comment" if is_comment else "Text", message)
        continue
    else:
        print "[VV] misc %s/0x%x " % (data[i], ord(data[i]))
        i += 1

    i += 1

if reached_end:
    print "[++] found %d fake newlines" % fake_newlines
    print "[++] payload is %d bytes (%d kilo bytes)" % (payload_length, payload_length/1024)
else:
    print "[--] something went wrong."


out_file.close ()
