import sys

def is_ascii(s):
    return all(ord(c) < 128 for c in s)



def verifyParamters(pmtsList):
    if len(sys.argv[1:]) == 9:
        extensions = ['tax', 'tax', 'txt']
        for k, v in enumerate(pmtsList[1:4]):
            v = v.replace('.\\', '')
            # Find where the extension starts
            index = v.index('.')
            # Verify if this file is with the right extension
            if extensions[k] != v[index + 1 :]:
                return False

    elif len(sys.argv[1:]) in [6, 7]:
        extensions = ['tax', 'txt']
        # print(pmtsList[1:3])
        for k, v in enumerate(pmtsList[1:3]):
            v = v.replace('.\\', '')
            # Find where the extension starts
            index = v.index('.')
            # print(v[index + 1:], k)
            # Verify if this file is with the right extension
            if extensions[k] != v[index + 1 :]:
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
            exit('Wrong delimiter!')
        else:
            return word
    # If len is 2, first character is \ and second isalpha()
    elif len(word) == 2 and word[0] == '\\' and word[1].isalpha():
        return replaceEscapeCode(word)
    else:
        exit('Wrong delimiter!')


def getPrefix(file, sep):
    return file.split('.')[0].split(sep)[0]


def getSuffix(file, sep):
    return file.split('.')[0].split(sep)[1]