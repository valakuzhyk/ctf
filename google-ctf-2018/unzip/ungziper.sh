set -e
gzip -l password.zip
zcat password.zip > nextPassword.zip
rm password.zip
mv nextPassword.zip password.zip
file password.zip