import random
import requests
import openai
import os
from dotenv import load_dotenv
import numpy as np
from morse import encode
load_dotenv()

openai.api_key = os.environ['API']
word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
paragraph = openai.Completion.create(
                engine="text-davinci-002",
                prompt="Generate a paragraph:",
                temperature=1,
                max_tokens=280
        )
WORDS = response.content.splitlines()

plaintext = paragraph.choices[0].text

# generate a random word from WORDS

def genRandomWord():
    return random.choice(WORDS).decode()

key = genRandomWord()
letters = "abcdefghijklmnopqrstuvwxyz"

# a mapping with a as index 0, b as index 1, etc.
lettermap = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}

# a mapping with 0 as 'a', 1 as 'b', etc.
numbermap = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'}

# a mapping of all vowels
vowels = ['a', 'e', 'i', 'o', 'u']

# a mapping of 'a' to 'z', 'b' to 'y', etc.
atbashmap = {'a': 'z' , 'b': 'y' , 'c': 'x' , 'd': 'w' , 'e': 'v' , 'f': 'u' , 'g': 't' , 'h': 's' , 'i': 'r' , 'j': 'q' , 'k': 'p' , 'l': 'o' , 'm': 'n' , 'n': 'm' , 'o': 'l' , 'p': 'k' , 'q': 'j' , 'r': 'i' , 's': 'h' , 't': 'g' , 'u': 'f' , 'v': 'e' , 'w': 'd' , 'x': 'c' , 'y': 'b' , 'z': 'a'}

def generateLetterMap(key):

    key = key.lower()

    # remove repeated letters
    key = "".join(dict.fromkeys(key))

    # find remaining letters of the alphabet
    for letter in letters:
        if letter not in key:
            key += letter

    return key

cipherlettermap = generateLetterMap(key)

# create a vigenere 2d array

def vigeneretable():
    table = []

    for i in range(26):
        row = []
        for j in range(26):
            row.append(letters[(i + j) % 26])
        table.append(row)
    
    return table

# create a playfair 2d array

def playfairtable():
    global key

    # regenerate key if it is too long
    if len(key) > 25:
        key = genRandomWord()

    key = key.lower()

    # remove repeated letters
    key = "".join(dict.fromkeys(key))

    # create a blank 5x5 table
    table = []
    for i in range(5):
        row = []
        for j in range(5):
            row.append("")
        table.append(row)
    
    flag = False
    # insert the key into the table
    for i in range(len(key)):
        # skip if letter is 'j'
        if key[i] == "j" or flag == True:
             # move back i by one
            j = i + 1
            # set flag to true
            flag = True
        else:
            j = i
        table[i // 5][i % 5] = key[j]

    flag = False
    # fill in the rest of the table from ciphermap
    for i in range(len(key), 25):
        # skip if letter is 'j' 
        if cipherlettermap[i] == "j" or flag == True:
            # move back i by one
            j = i + 1
            # set flag to true
            flag = True
        else:
            j = i
        table[i // 5][i % 5] = cipherlettermap[j]
    
    return table

# remove all punctuation from plaintext
def removepunctuation(plaintext):
    ciphertext = ""
    
    for char in plaintext:
        
        if char.isalpha():
            ciphertext += char
    
    return ciphertext.lstrip()

def plaintextsplit(plaintext):
    plaintext = plaintext.lower()
    
    # if plaintext has two same letters in a row, add x between them
    for i in range(len(plaintext) - 1):
        if plaintext[i] == plaintext[i+1]:
            plaintext = plaintext[:i+1] + "x" + plaintext[i+1:]
    
    # if plaintext length is odd, add a z to the end
    if len(plaintext) % 2 == 1:
        plaintext += "z"
    
    # split plaintext into pairs
    plaintext = [plaintext[i:i+2] for i in range(0, len(plaintext), 2)]
    return plaintext

# find elements in a 2d array
def find(array, element):
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == element:
                return i, j
    return -1, -1

# make a 3x3 matrix from the key

def generateHill():

    global key
    key = key.lower()
    
    # if length is lower than 9, add the letters of the alphabet to the end until the length is 9
    if len(key) < 9:
        for i in range(len(key), 9):
            key += letters[i]
    
    # if length is greater than 9, remove the extra letters
    if len(key) > 9:
        key = key[:9]
    
    # create a blank 3x3 matrix
    table = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append("")
        table.append(row)
    
    # insert the ASCII value of the key into the table
    for i in range(len(key)):
        table[i // 3][i % 3] = lettermap[key[i]]

    return table

##############################################################################################################################

# ENCRYPTION

def caesar(plaintext):
    ciphertext = ""
    shift = random.randint(0, 25)
    
    for char in plaintext:
        
        if char.isalpha():
            
            if char.isupper():
                ciphertext += chr((ord(char) + shift - 65) % 26 + 65)
            
            else:
                ciphertext += chr((ord(char) + shift - 97) % 26 + 97)
        
        else:
            ciphertext += char
    
    return ciphertext.lstrip(), shift, "Caesar"


def monoalphabetic(plaintext):
    ciphertext = ""
    
    for char in plaintext:
        
        if char.isalpha():
            
            if char.isupper():
                char = char.lower()
                index = letters.index(char)
                ciphertext += cipherlettermap[index].upper()
            
            else:
                index = letters.index(char)
                ciphertext += cipherlettermap[index]
        
        else:
            ciphertext += char
    
    return ciphertext.lstrip(), key, "Monoalphabetic"


def vigenere(plaintext):
    ciphertext = ""
    global key
    keycopy = key
    table = vigeneretable()
    
    for char in plaintext:
        
        if char.isalpha():
            
            if char.isupper():
                char = char.lower()
                index = letters.index(char)
                ciphertext += table[index][letters.index(key[0])].upper()
                key = key[1:] + key[0]
            
            else:
                index = letters.index(char)
                ciphertext += table[index][letters.index(key[0])]
                key = key[1:] + key[0]
        
        else:
            ciphertext += char
    
    return ciphertext.lstrip(), keycopy, "Vigenere"

def playfair(plaintext):
    ciphertext = ""
    global key
    keycopy = key
    table = playfairtable()
    plaintextcopy = plaintext
    
    # remove punctuation
    plaintext = removepunctuation(plaintext)
    
    # split the plaintext 
    splitarray = plaintextsplit(plaintext)
    
    for i in range(len(splitarray)):
        
        # find both elements in the table
        row1, col1 = find(table, splitarray[i][0])
        row2, col2 = find(table, splitarray[i][1])
        
        # if the two elements are in the same row
        if row1 == row2:
            # take the letter to the right of the letter
            ciphertext += table[row1][(col1 + 1) % 5]
            ciphertext += table[row2][(col2 + 1) % 5]
        
        # if the two elements are in the same column
        elif col1 == col2:
            # take the letter below the letter
            ciphertext += table[(row1 + 1) % 5][col1]
            ciphertext += table[(row2 + 1) % 5][col2]
        
        # if the two elements are not in the same row or column
        else:
            # take the letter in the same row but to the left of the letter
            ciphertext += table[row1][col2]
            # take the letter in the same column but above the letter
            ciphertext += table[row2][col1]
    
    for i in range(len(plaintextcopy)):
        
        if plaintextcopy[i].isalpha() == False:
            ciphertext = ciphertext[:i] + plaintextcopy[i] + ciphertext[i:]
        
        if plaintextcopy[i].isupper():
            ciphertext = ciphertext[:i] + ciphertext[i].upper() + ciphertext[i+1:]

    return ciphertext.lstrip(), keycopy, "Playfair"

def hill(plaintext):
    ciphertext = ""
    global key
    keycopy = key
    table = generateHill()
    plaintextcopy = plaintext
    matrices = []
    # remove spaces
    plaintext = removepunctuation(plaintext)
    plaintext = plaintext.lower()
    # split the plaintext into groups of 3
    chunks = [plaintext[i:i+3] for i in range(0, len(plaintext), 3)]
    
    # for each group of 3, convert into a 1x3 matrix
    for i in range(len(chunks)):
        # if length is less than 3, add letters to the end until length is 3
        if len(chunks[i]) < 3:
            for j in range(len(chunks[i]), 3):
                chunks[i] += letters[j]
            # add the matrix to the list
        matrices.append([lettermap[chunks[i][0]], lettermap[chunks[i][1]], lettermap[chunks[i][2]]])
    
    result = []
    # for each matrix, multiply by the key matrix
    for i in range(len(matrices)):
        result.append([(matrices[i][0] * table[0][0] + matrices[i][1] * table[0][1] + matrices[i][2] * table[0][2])%26,
                       (matrices[i][0] * table[1][0] + matrices[i][1] * table[1][1] + matrices[i][2] * table[1][2])%26,
                       (matrices[i][0] * table[2][0] + matrices[i][1] * table[2][1] + matrices[i][2] * table[2][2])%26])
    
    # for each matrix, convert back to a letter
    for i in range(len(result)):
        ciphertext += letters[result[i][0]]
        ciphertext += letters[result[i][1]]
        ciphertext += letters[result[i][2]]
    
    for i in range(len(plaintextcopy)):
        if plaintextcopy[i].isalpha() == False:
            ciphertext = ciphertext[:i] + plaintextcopy[i] + ciphertext[i:]
        
        if plaintextcopy[i].isupper():
            ciphertext = ciphertext[:i] + ciphertext[i].upper() + ciphertext[i+1:]

    return ciphertext.lstrip(), keycopy, "Hill"
    
def affine(plaintext):
    ciphertext = ""
    x, y = random.random(), random.random()
    x, y = int(x * random.randint(100,1000)), int(y * random.randint(100,1000))
    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                char = char.lower()
                ciphertext += numbermap[((x*lettermap[char]) + y) % 26].upper()
            else:
                ciphertext += numbermap[((x*lettermap[char]) + y) % 26]
        else:
            ciphertext += char
    
    return ciphertext.lstrip(), (x, y), "Affine"

# NOT DONE FULLY
def piglatin(plaintext):
    ciphertext = ""
    plaintextcopy = plaintext
    plaintext = plaintext.replace(".", "")
    plaintext = plaintext.replace(",", "")
    plaintext = plaintext.replace("!", "")
    plaintext = plaintext.replace("?", "")
    plaintext = plaintext.replace("'", "")
    plaintext = plaintext.replace("\"", "")
    plaintext = plaintext.replace(";", "")
    plaintext = plaintext.replace(":", "")
    plaintext = plaintext.replace("-", "")
    plaintext = plaintext.replace("_", "")
    plaintext = plaintext.replace("/", "")
    plaintext = plaintext.replace("(", "")
    plaintext = plaintext.replace(")", "")
    plaintext = plaintext.replace("[", "")
    plaintext = plaintext.replace("]", "")
    plaintext = plaintext.replace("{", "")
    plaintext = plaintext.replace("}", "")
    plaintext = plaintext.split()
    for word in plaintext:
        # if the first letter is a vowel
        # if the first letter is capitalized, convert to lowercase
        if word[0].isupper():
            word = word.lower()
            if word[0] in vowels:
                ciphertext += word[0].upper() + word[1:] + "yay" + " "
            else:
                ciphertext += word[1].upper() + word[2:] + word[0] + "ay" + " "
        else:
            if word[0] in vowels:
                ciphertext += word[0] + word[1:] + "yay" + " "
            else:
                ciphertext += word[1] + word[2:] + word[0] + "ay" + " "
    
    # implemment adding punctuation
    for i in range(len(plaintextcopy)):
        pass
           
    return ciphertext.lstrip(), "Pig Latin"

def atbash(plaintext):
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                char = char.lower()
                ciphertext += atbashmap[char].upper()
            else:
                ciphertext += atbashmap[char]
        else:
            ciphertext += char
    return ciphertext.lstrip(), "Atbash"

def morsecode(plaintext):
    plaintext = plaintext.upper()
    plaintext = removepunctuation(plaintext)
    ciphertext = encode(plaintext)
    return ciphertext.lstrip(), "Morse Code"


##############################################################################################################################

# DECRYPTION