set -e
unzip -t password.zip
echo "Unzipping to get"
unzip -l password.zip
unzip -p password.zip > nextPassword.zip
rm password.zip
mv nextPassword.zip password.zip
file password.zip