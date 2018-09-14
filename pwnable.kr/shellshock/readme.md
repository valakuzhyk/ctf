# Stuck
The only directions I can think to go in
* Bash is somehow important, why else would the include it?
* The uid/gid is important. It just sets my id to my group id.

# Solution
CVE-2014-6271 indicates that we can add a bash function to an environment variable, and it will get executed when invoking bash. Since bash is invoked with a higher level of privilege, it can read the contents of the flag