Got a little better. Understood what I think is the meaning of heap feng shui.

Did need a little help, since I was allocating too much memory, meaning that my allocation site was not in the same place as the newly deleted objects, making it extremely hard (read: "impossible as far as I know") to get the UAF to work.

# Notes

Location of give_shell: 0x40117a
Location of vtable:     0x401550

However, the structure contains the following
Stack pointer to object on heap-> first element is pointer to vTable -> 2 element is pointer to code

If we choose the right amount of data, the allocation will happen over the deleted objects. This will cause us to write to the pointer to the vtable.
So, in the file, we should write 8 bytes, containing an address 8 bytes less than the vTable, 


Location of the man struct on heap:   0x230d c50
Location of the woman struct on heap: 0x230d cA0
End of the woman struct is            0x230d cc0

Location of the data on heap:         0x230e  cA0


This run, man is at [ebp + 38], and the first function is the shell script, so if I can write data into the program,
I can potentially overwrite what used to be the objects, so that they access the normally not accessed field.
