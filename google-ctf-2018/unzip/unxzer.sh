set -e
unxz -l password.zip
xzcat password.zip > nextPassword.zip
rm password.zip
mv nextPassword.zip password.zip
file password.zip