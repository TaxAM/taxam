import sys

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def verifyExtension(files, extention):
    for file in files:
        if file != None and extention != file.split('.')[-1]:
            return False
    return True



def printDict(dict):
    for k, v in dict.items():
        print(k, v)


global c
c = 0
def addInMatrix(matrix, taxon, level=5):
    global c
    try:
        c += 1
        matrix[taxon[level]] += 1
    except:
        c += 1
        matrix[taxon[level]] = 1



def replaceEscapeCode(word):
    if word == r'\b':
        return '\b'
    elif word == r'\t':
        return '\t'
    elif word == r'\n':
        return '\n'
    elif word == r'\a':
        return '\a'
    elif word == r'\r':
        return '\b'
    else:
        return word

def validDelimiter(word):
    # If len is just 1
    if len(word) == 1:        
        if not is_ascii(word):
            print('Wronge delimiter: ' + word)
            exit()
        else:
            return word
    # If len is 2, first character is \ and second isalpha()
    elif len(word) == 2 and word[0] == '\\' and word[1].isalpha():
        return replaceEscapeCode(word)
    else:
        print('Wronge delimiter: ' + word)
        exit()


def getPrefix(file, sep):
    return file.split('.')[0].split(sep)[-2]


def getSuffix(file, sep):
    return file.split('.')[0].split(sep)[-1]