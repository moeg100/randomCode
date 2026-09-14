from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


# This is for a challenge in seed lab.


plain_data = b"This is a down secret."
print(len(plain_data))
#custom_iv = b"aabbccddeeff00998877665544332211" python treat it as 32 byte
custom_iv = bytes.fromhex("aabbccddeeff00998877665544332211")
#target_cipher_text = bytes.fromhex("c31b94f92afaadc587c4847bd38e1407")
target_cipher_text = bytes.fromhex("764aa26b55a4da654df6b19e4bce00f4ed05e09346fb0e762583cb7da2ac93a2")

padded_data = pad(plain_data, 16)

#print(len(file_data))

with open("words.txt", "r") as k:
	content = k.read().split()
#	print(content)



for word in content:
	wordByte = word.encode("ascii")
	wordLength = len(word)
	if wordLength <= 16:
		paddingLength = 16 - wordLength
		if paddingLength == 0:
			paddingLength = 16
		guess_key = wordByte+(b'\x23' * paddingLength)
		try:
			cipher = AES.new(guess_key, AES.MODE_CBC, iv=custom_iv)
			ciphertext = cipher.encrypt(padded_data)
			if ciphertext == target_cipher_text:
				print(f"Found the Key {guess_key.hex()}, with the word {word}")
				break
		except:
			print("something gone wrong")
else:
	print("key was not found")
