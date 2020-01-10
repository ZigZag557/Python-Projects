
def rot13(message):
	alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	retTxt = ""

	for x in message:

		if not x.isalpha():
			retTxt += x

		alpIndx = alphabet.index(x.lower())

		if x.isupper():
			retTxt += alphabet[(alpIndx + 13) % 25].upper()
		else:
			retTxt += alphabet[(alpIndx + 13) % 25]

return retTxt



