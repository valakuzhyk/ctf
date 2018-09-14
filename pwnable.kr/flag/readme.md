I managed to solve this one on my own due to my previous knowledge on upx.

By unpacking, and then disassembling, you can identify the code that is run, and then look at the memory location that is output from malloc.

The way the video does it is by breakpointing on a system call that is found via strace, and then dumping memory. From there, you can do an inspection of memory (we could also dump the code and do disassembly then.)