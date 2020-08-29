import string
import sys
import re

with open("words_alpha.txt", "r") as f:
	words = f.read().splitlines()

# convert numeric ciphertext into alphabetic
def convertNumberCiphertext():
	ciphertext = """7 12 26 20   14 4   22 4 15   14 4   7 12 3 2   22 4 15   12 26 16 3   2 15 6 3 24 25 5   5 4 14 3 23 

	24 26 20 12 3 24   20 12 26 2   26 8 9 12 26 18 3 20 25 5 ?  

	26 2 23 7 3 24 :   20 12 3   23 26 6 3   20 12 25 2 10 .   23 25 6 9 8 3   23 15 18 23 20 26 20 25 4 2 23  

	24 3 9 8 26 5 3   4 2 3   23 22 6 18 4 8   4 21   9 8 26 25 2 20 3 17 20   7 25 20 12   4 2 3  

	23 22 6 18 4 8   4 21   5 25 9 12 3 24 20 3 17 20 ."""

	ciphertext = " ".join(ciphertext.split('\n'))
	cipherAlpha = ""
	alphabet = string.ascii_lowercase

	a1 = ciphertext.split("  ")
	a2 = []
	for each in a1:
		a3 = each.split()
		a2.append(a3)

	for word in a2:
		if len(word) > 0:
			for char in word:
				if char.isnumeric():
					cipherAlpha += alphabet[int(char) - 1]
				else:
					cipherAlpha += char
			cipherAlpha += " "

	return(cipherAlpha)
# ciphertext = "KCXCHUHCRIB KCGO RIKA CI RDW XCITB. QDH CP YO DBO RDW CXUZCIUHCRIB, RDW JRBBCQCKCHCOB QOVRXO KCXCHKOBB. —FUXCO JURKCIOHHC".lower()
# ciphertext = "glzt nd vdo nd glcb vdo lzpc bofcxye edncw xztlcx tlzb zhilzrctye? zbwgcx: tlc wzfc tlybj. wyfihc worwtztydbw xcihzec dbc wvfrdh du ihzybtcqt gytl dbc wvfrdh du eyilcxtcqt."
ciphertext = convertNumberCiphertext()

# please don't judge this, it hurts me too
# just making the ciphertext easier to work with
ciphertext_clean = ""
for char in ciphertext:
	if char.isalpha():
		ciphertext_clean += char
	elif char == " ":
		ciphertext_clean += char
print("Ciphertext --> " + ciphertext_clean)
cipher_words_list = ciphertext_clean.split()
cipher_words = sorted(cipher_words_list, key=len)
cipher_words.reverse()

# the main mapping dictionary
mapping = {}

# convert word to alphabetic pattern
def word2pattern(word):
	alphabet = string.ascii_lowercase
	buildPattern =  ""
	dic = {}
	i = 0
	for letter in word:
		# if we haven't seen the letter yet
		if letter not in dic.keys():
			# add to lookup dictionary
			# assign next unused letter from alphabet
			dic[letter] = alphabet[i]
			# also add that alphabetical letter
			# to our output string
			buildPattern = buildPattern + alphabet[i]
			# iterate to next alphabet letter
			i += 1
		else: # if we have seen the letter already
			# look up assigned buildPattern letter in dic
			buildPattern = buildPattern + dic[letter]

	return(buildPattern)

# match pattern/word to list of words
def pattern2word(pattern):
	matching_words = []
	for word in words:
		if word2pattern(word) == word2pattern(pattern):
			matching_words.append(word)

	return(matching_words)

# map letters of a cipher word to the real word
def addMapping(match, cipherWord):
	i = 0
	for letter in match:
		mapping[cipherWord[i]] = letter
		i += 1

# - see if any cipher words math with a single real word
# - if yes, add it to mapping dictionary
# - if none fully match, return list of cipher words
#   that have less than 6 potential matches
def fullMatches():
	hasThereBeenAMatch = False
	lessThanSix = []
	for cipher in cipher_words:
		# get all possible matches
		results = pattern2word(cipher)

		if len(results) == 1:
			hasThereBeenAMatch = True
			addMapping(results[0], cipher)
			# remove matched cipher word from cipher word list
			# so we don't use/match it again
			cipher_words.remove(cipher)
		elif len(results) < 6:
			lessThanSix.append(cipher)

	return(hasThereBeenAMatch, lessThanSix)

# - create regex to match half-matched cipher words
#   to potential real words
# - if all letters are matched, we don't need regex searching 
def makeRegex(cipher):
	fullWordMatch = True
	# denote start of line
	regWord = "^"
	# add chars
	for letter in cipher:
		# if char is already mapped add it
		if letter in mapping.keys():
			regWord += mapping[letter]
		# if char isn't mapped, use the regex '.'
		# to match any char
		else:
			regWord += "."
			fullWordMatch = False
	# denote end of line
	regWord += '$'

	if fullWordMatch: # if no regex was needed
		return("fullWordMatch")
	else:
		return(regWord)

# use the regex to match potential words
def getRegexMatches(regex, cipher):
	m = []
	for word in words:
		if re.search(regex, word):
			m.append(word)

	return(m)

# map any regex matches to dictionary
def mappingMatches():
	hits = []
	for cipher in cipher_words:
		regex = makeRegex(cipher)
		# if no regex needed and full cipher word is mapped
		# YAY
		if regex == "fullWordMatch":
			hits.append(cipher)
		else:
			# get rexex matches
			regexMatches = getRegexMatches(regex, cipher)
			# if only one, SWEET
			if len(regexMatches) == 1:
				addMapping(regexMatches[0], cipher)
				hits.append(cipher)

	return(hits)

# - map cipher chars to real chars
# - functionality to guess your own mapping
#   in event not everything is solved on its own
def decode(ciphertext, end=False):
	decoded_message = ""

	for char in ciphertext:
		if char.isalpha(): # if it's an actual char
			# if it is in the mapping dic
			if char in mapping.keys():
				# add it to our decoded message
				decoded_message += mapping[char]
			else: # if it isn't in the mapping dic
				# denote what cipher char is in its place
				decoded_message += "[{}]".format(char)
		else: # not a normal char, so like -,+?:.
			# just add it where it's supposed to go
			decoded_message += char

	print(decoded_message)

	# if not the end of decoding, ask for any cipher mapping guesses
	if not end:
		guesses = input("\nDo you have any guesses?\nFormat: cipherChar:guess,cipherChar:guess\nType 'n' for no -> ")

		# populate mapping dic with guesses
		if guesses != 'n':
			x = guesses.split(',')
			for each in x:
				y = each.split(':')
				mapping[y[0]] = y[1]

			print('\n')
			# decode further with new additions to mapping dic
			decode(ciphertext)

# - see if we have any full matches 
#   if we do they are auto-added to mapping dic
fullMatch, options = fullMatches()
# - if we don't, print out cipher words that matched
#   to less than 6 words and let the user decide
#   which one to test
if not fullMatch:
	print("\n !!!!! No full matches !!!!!\n")
	# for each cipher word with < 6 matches
	for option in options:
		print(option + ":")
		# print out their potential matches
		print(pattern2word(option))

	guesses = input("\nDo you have any guesses?\nFormat: cipherWord:guessWord\nType 'n' for no -> ")

	if guesses != 'n':
		x = guesses.split(':')
		# map the user's guessed cipher word:real word
		addMapping(x[1],x[0])

j = 0
# - while there are still undeciphered words
#   match, add mapping, match again, etc.
while(len(cipher_words) > 0):
	hits = mappingMatches()
	if len(hits) > 0:
		for hit in hits:
			# remove deciphered words
			cipher_words.remove(hit)

		j += 1
	# if not more cipher words match, end it
	else:
		break

# pretty output
print("==== FINISHED ====")
print("Letter Mapping: ")
for key in sorted(mapping.keys()):
	print("{}: {}".format(key, mapping[key]))
print("\nCipher Words That Aren't Cracked:")
print(cipher_words)
# print('\n')
print("~~~~ DECODED MESSAGE ~~~~")

# decode the ciphertext
decode(ciphertext)

print("\n<><><><><><><><><><><><><><><><><><>")
print("\n(☞ﾟヮﾟ)☞ FINAL RESULTS ☜(ﾟヮﾟ☜)")
print("Letter Mapping: ")
for key in sorted(mapping.keys()):
	print("{}: {}".format(key, mapping[key]))
print("\n==== DECODED MESSAGE ====")

# final decoded ciphertext 
decode(ciphertext, True)