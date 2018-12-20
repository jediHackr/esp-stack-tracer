Import("env")

def processStackTrace(source, target, env):
    print "Paste the core dump information (Ctrl+d or Ctrl+z to end):"
    stack = []
    try:
        while True:
            stack.append(raw_input())
    except EOFError:
        pass
    
    print "Processing stack trace..."
    addresses = []
    for line in stack:
        if line.startswith('Backtrace: '):
            #Start pulling addresses out.
            addStack = line[11:].split(' ')
            addresses.extend([pair.split(':') for pair in addStack])
    
    if len(addresses):
        env.Execute("xtensa-esp32-elf-addr2line -aipfC -e $BUILD_DIR/${PROGNAME}.elf " + " ".join([a[0] for a in addresses]))
    else:
        print "No backtrace found to process.\nExiting."


env.AlwaysBuild(env.Alias("stack",
    "$BUILD_DIR/${PROGNAME}.elf", processStackTrace))
    #["xtensa-esp32-elf-addr2line -aipfC -e $BUILD_DIR/${PROGNAME}.elf 0x4010923e 0x3ffb71d0"]))

"""
Guru Meditation Error: Core  1 panic'ed (InstrFetchProhibited). Exception was unhandled.
Core 1 register dump:
PC      : 0x00000000  PS      : 0x00060130  A0      : 0x80109241  A1      : 0x3ffb7190
A2      : 0x3ffbecc4  A3      : 0x3ffbf3e4  A4      : 0x3ffbc228  A5      : 0x3ffbc0e4
A6      : 0x0204a8c0  A7      : 0x6504a8c0  A8      : 0x801090e0  A9      : 0x3ffb7150
A10     : 0x3ffbecd4  A11     : 0x3ffbf3e4  A12     : 0x3ffb719c  A13     : 0x00000044
A14     : 0x00000001  A15     : 0x00000006  SAR     : 0x00000010  EXCCAUSE: 0x00000014
EXCVADDR: 0x00000000  LBEG    : 0x4000c349  LEND    : 0x4000c36b  LCOUNT  : 0x00000000

Backtrace: 0x00000000:0x3ffb7190 0x4010923e:0x3ffb71d0 0x401111f1:0x3ffb71f0 0x40113d9d:0x3ffb7230 0x40119bce:0x3ffb7250 0x40108601:0x3ffb7270
"""