package main

import (
	"strconv"
	"strings"
	"encoding/base64"
	"encoding/hex"
	"io/ioutil"
	"log"
	"math/bits"
)

func main() {
	a := "[JFKDNZQUWPYOVBETHRXLSCGIAM, 16, HCPSU H OAXPNUE, WIHUZSD ENYU JDACS]"
	replaceAlpha(a)
}

func replaceAlpha(s string) {


	s = strings.TrimPrefix(s, "[")
	s = strings.TrimSuffix(s, "]")
	fields := strings.SplitN(s, ", ", 3)
	newAlphabet := fields[0]
	rot, err := strconv.Atoi(fields[1])
	if err != nil {
		log.Fatal("Problem decoding", err)
	}
	cipherText := fields[2]

	plaintext := ""
	for _, c := range cipherText {
		plaintext += replaceChar(string(c), rot, newAlphabet)
	}
	log.Println(plaintext)
}

func replaceChar(c string, r int, newAlphabet string) string {
	alphabet := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

	idx := strings.Index(newAlphabet, c)
	if idx == -1 {
		return c
	}
	return string(alphabet[(idx + 26 - r) % 26])
}


func writeImageEncodedFile(fileName string) {
	bytes, err := ioutil.ReadFile(fileName)
	if err != nil {
		log.Fatal("can't read file", err)
	}
	fullFile := string(bytes)
	colors := strings.Split(fullFile, "bgcolor=\"#")
	newFileBytes := []byte{}
	for _, s := range colors {
		if strings.HasPrefix(s, "<") {
			continue
		}
		color := s[0:6]
		bytes, err := hex.DecodeString(color)
		if err != nil {
			log.Println(err)
			log.Fatal("Couldn't decode bytes: ", s)
		}
		newFileBytes = append(newFileBytes, bytes...)
	}

	err = ioutil.WriteFile("elfFile", newFileBytes, 0644)
	if err != nil {
		log.Fatal("Could not write output", err)
	}
}

func writebase64File(s string) {
	bytes, err := base64.StdEncoding.DecodeString(s)
	if err != nil {
		log.Fatal("unable to base64 decode this shit ", err)
	}
	err = ioutil.WriteFile("png2.png", bytes, 0644)
	if err != nil {
		log.Fatal("unable to write to file ", err)
	}
}

func encrypt(key, plaintext string) string {
	plaintext += "\x00"
	cipher := ""
	for i := range plaintext {
		x := int(key[i%len(key)])
		cipher = cipher + string(int(plaintext[i])^int(key[(i+x)%len(key)]))
	}
	return cipher
}

func decrypt(ciphertext string) string {
	return ""
}

func NormalizedHammingDistance(N int, bytes []byte) {
	normalizedDist := 0
	for i := 0; i+2*N < len(bytes); i += N {
		dist := HammingDistance(bytes[i:i+N], bytes[i+N:i+2*N])
		normalizedDist += dist
	}
}

func HammingDistance(b1, b2 []byte) int {
	if len(b1) != len(b2) {
		log.Fatal("Did not pass same size b1 and b2")
	}
	dist := 0
	for i := range b1 {
		dist += bits.OnesCount8(uint8(b1[i] ^ b2[i]))
	}
	return dist
}
