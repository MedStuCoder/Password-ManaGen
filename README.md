# Password-ManaGen
This is neither a password manager (as in saving your passwords somewhere) nor simply a random password generator but both at the same time. The main focus is to NOT STORE ANY kind of data pertaining to your passwords.

It accepts a master password from which a Base32 token for an [HOTP algorithm](https://en.wikipedia.org/wiki/HMAC-based_One-Time_Password) is securely (hashed and salted) generated.
It then asks for an "Account Name" which is also hashed to generate a Counter number for the HOTP.
Then the output of the HOTP is also hashed and from the hash multiple index numbers are derived to look up in a [Diceware](https://en.wikipedia.org/wiki/Diceware) compatible wordlist
(Any wordlist works really, but since Diceware is the standard for password it is used).

The [EFF Wordlist](https://www.eff.org/dice) is built into the code but as mentioned you can use any diceware compatible wordlist or even others such as Bitcoin's [Bip39 wordlists](https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md) Although the latter would need some small modifications to the code.
You can use [Wordlist_to_JSON](https://gist.github.com/MedStuCoder/1fe47de8501e56b2feb0c2a30e91d07b) to convert other Diceware lists to JSON to use with the code.

The words are selected from the wordlist and some modifications such as capitalizing specific letters (based on the password+key hash) and adding some special characters including numbers (again, in a repeatable manner) are applied and the final password is printed out. More details can be found in the code's comments.

The result will be the same given the correct master password and account name, there are no "wrong" results as the code is completely blind and does not store anything.

The only dependency is [PyOTP](https://pypi.org/project/pyotp/).

This code is published with the hopes that it can be useful by being put into use for real world "Password manager" apps and softwares.

