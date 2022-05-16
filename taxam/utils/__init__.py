"""Library with generic tools to me used in taxam project.

Functions
---------
isAscii(s)
verifyExtension(files, extention)
printDict(dict)
addInMatrix(matrix, taxon, level=5)
replaceEscapeCode(word)
validDelimiter(word)
getPrefix(file, sep)
getSuffix(file, sep)
returnIntegerList(string = '')
"""
import sys

def isAscii(word):
    """Check if all characters of this words are an ascii character.

    Parameters
    ----------
    word : str
        Word to be verified.

    Returns
    -------
    bool
        True if all characters are ascii characters,or false, if not..
    """
    return all(ord(character) < 128 for character in word)

def verifyExtension(files, extention):
    for file in files:
        if file != None and extention != file.split('.')[-1]:
            return False
    return True


def printDict(dict):
    for k, v in dict.items():
        print(k, ' -> ', v)


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
        if not isAscii(word):
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


def returnIntegerList(string = ''):
    tmp_list = string.split(',')
    final_list = {}
    for item in tmp_list:
        try:
            if item != '':
                k, v = item.split(':')
                final_list[k] = int(v)
        except:
            sys.exit('One or more items from reads quantity are not integer. Or invalid key.')
    return final_list.copy()