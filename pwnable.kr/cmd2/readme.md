#Stuck
I need to get a command run to dump this flag's contents, but the environment has been erased (including path), and I can't use '/' character. The question is how to do that.

#Solution
There are builtin commands to bash. After reading that much, I started reading the commands that are available. the "command" command allows you to use the default value of the path variable, so that you can at least get the typical location of the linux utilities. Using that, I can get the same solution as before, simply "cat f*"