#pylint:disable=W0622
from pyotp import HOTP
from json import loads
from textwrap import wrap
from hashlib import sha3_512
from base64 import b32encode
from time import sleep


        
def jsonhandler(indx): #Reads the requested words from the wordlist
	
	file = "eff_large_wordlist.json"
	
	with open (file, "r") as content:
		data = loads(content.read()) #Or load(content)
	return (data[indx])
	


def otpgen(ky,keyring): #Main part of the OTP generator, see "Generate" function
	
	hotp = HOTP(keyring)
	return (hotp.at(ky))



def xor_two_str(str1,str2): #Extra safety feature, see below in "Generate" function
    a = int(str1, base=16)
    b = int(str2, base=16)
    return hex(a ^ b).encode()



def Generate(key):
	defaultWordsCount = "5"
	charslist=R'''!#$%^&*()-=+[]{}:;\"'<>?/0123456789''' #Special Characters List, can be modified
	
	password = input("Password? : ")
	passhash=sha3_512()
	passhash.update(password.encode())
	passhash=passhash.hexdigest() #Hashing the pw
	del password #So that the plaintext pw doesn't hang around in RAM until it's garbage collected.
	
	keyhash = sha3_512()
	keyhash.update(str(key).encode())
	keyhash = keyhash.hexdigest()

	keyring = b32encode(xor_two_str(passhash, keyhash)) #The hashed password and the hashed key are XORed together for good measure 
	#(Even if the hashing algorithm is broken the password will not be recoverable)
	#and converted to the Base32 string the OTP algorithm needs as token.
	

	hash =	sha3_512()
	hash.update(otpgen(key, keyring).encode())
	#The resulting OTP number is hashed and the resulting letters are used to generate indexes 
	#which will be used to choose words from the wordlist.
	
	hash=hash.hexdigest()
	#hashascii=''.join(str(ord(ch)) for ch in hash)	
	
	hashascii=1
	for ch in hash:
		hashascii *= int((ord(ch)**3)/1.61803) #Non random changes to the resulting ASCII decimals
	
	hashascii=str(hashascii)
	
	#This next piece is to make sure the generated indexes are compatible with Diceware numbers
	for ch in range(7, 10):
		hashascii=hashascii.replace(str(ch), '')
	hashascii=hashascii.replace("0",'')
	
	try:
		words = int(input("How many words ? :") or defaultWordsCount)
	except ValueError:
		print("Bad input; Using default word count of", defaultWordsCount)
		sleep(0.5)
		words=int(defaultWordsCount)
	hashes=wrap(hashascii,5)
	hashes=hashes[:words]  #Getting the necessary number of indexes for the words
	
	exportlist=[]
	for hash in hashes:
		try:	
			spec = wrap(hash, 1) #This is a token that we can trust that will always be the same
			#given the same key and password so we can do whatever we want with it to the generated password
			#like adding special characters or capitalizing some letters or whatever.
			
			exportlist.append(jsonhandler(hash)) #Getting the words
			
			if int(spec[2])%2 == 0: #Adding some capital letters to the generated password
				exportlist[-1]=exportlist[-1].capitalize()
				
			
		except KeyError as e:
			print(e)
		except IndexError as a:
			print(a)
			
	exportlist.append(charslist[(int(spec[0])*int(spec[1])) - (37 - len(charslist))]) #Adding special characters.
	#37 is 6*6+1 and 6*6 is because the higest number in a Diceware index is 6 and the +1 is for compatibility with list index.
	#The whole code here makes sure it generates a correct index number for the special characters list.
	exportlist.append(charslist[(int(spec[3])*int(spec[4])) - (37 - len(charslist))]) #Another one :)
	
	print()
	print("Your password:", ''.join(exportlist))
	print() #Print the final generated password
		
		
		
		
def main(string):
	#The account name is first hashed and then converted to an integer made up of the ascii
	#decimal representations of its letters, then passed to the HOTP as the key index.
	
	hash=sha3_512()
	hash.update(string.encode())
	hash=hash.hexdigest()
	asciiList = []
	for char in hash:
		 asciiList.append(str(ord(char)))
		 
	Generate(int("".join(asciiList)))

#Demo:
while True:
	main(input("Account Name? : "))
	sleep(1)
		
	
