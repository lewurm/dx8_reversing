#!/usr/local/bin/python2

import sys, struct

with open(sys.argv[1], "r") as fd:
    data = fd.read()

out_file = open(sys.argv[1].replace(".sax", ".s"), "wb")
out_file.write(".text\n")

# input is a string consisting of two chars, representing a byte in hex
def out_byte(byte_string):
    assert (len(byte_string) == 2)
    val = int(byte_string, 16)
    out_file.write(".byte 0x" + byte_string + "\n")
    # out_file.write(struct.pack('1B', *[val]))
    return val

def out_word(byte_string):
    assert (len(byte_string) == 8)
    val = out_byte(byte_string[0:2])
    val = out_byte(byte_string[2:4])
    val = out_byte(byte_string[4:6])
    return (val + out_byte(byte_string[6:8])) % 0x100

def out_chunk(addr, byte_string):
    # 0x100 bytes + 1 byte checksum -> 0x200 chars + 2 chars checksum
    assert (len(byte_string) <= 0x202)
    plen = len(byte_string[2:])
    checksum = int(byte_string[0:2], 16)
    i, j, val = 0, 0, 0
    val += int(addr[0:2], 16)
    val += int(addr[2:4], 16)
    val += int(addr[4:6], 16)
    val += int(addr[6:8], 16)
    i += 2
    while i < plen:
        val = (val + out_word(byte_string[i:i+8])) % 0x100
        i += 8
    print "[XXX] checksum 0x%02x (0x%02x) vs. 0x%02x (0x%02x)" % (val, ~val & 0xff, checksum, ~checksum & 0xff)
    return val


data_length = len(data)

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
        print "[++] writing 0x100 bytes at addr 0x%s " % addr
        out_file.write(".org 0x%s\n" % addr)
        payload_length += 0x100
        real_length = 0
        i += 8
        # for j in [1,2,3,4]:
        #     print "> 0x%s" % data[i:i+8]
        #     i += 8 
        #     real_length += 8
        chunk = ""
        while real_length < (0x101 * 2) and ord(data[i]) != 0x1a:
            chunk += data[i]
            i += 1
            real_length += 1
        if real_length == 0x202:
            out_chunk(addr, chunk)
        else:
            print "XXX TODO"
        print "[++] got %d / 0x%x bytes of data after addr -> checksum 0x%s" % (real_length/2, real_length/2, data[i:i+2])
        i += 2
        if real_length < 0x200:
            print "[--] you should see this message only once"
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
