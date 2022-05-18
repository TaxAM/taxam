"""Library with generic tools to me used in taxam project.

Functions
---------
isAscii(s) : bool
    Check if all characters of this words are an ascii character.
verifyExtension(files, extention)
    Verify if the files have the right extension.
printDict(dict)
    Prints a dict in the format: <key> -> <value>\\n
addInMatrix(matrix, taxon, level)
    Adds the counting of a animal to dict matrix.
replaceEscapeCode(word)
    Replace a str escape code for a real escape code.
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
    """Verify if the files have the right extension.

    Parameters
    ----------
    files : str[]
        A list  with all the file paths to be verified.
    extention : str
        Extension to verify match.

    Returns
    -------
    bool
        If all the files match with the right extension, it returns True,
        if just one don't match, it return False.
    """    
    for file in files:
        if file != None and extention != file.split('.')[-1]:
            return False
    return True


def printDict(dict):
    """Prints a dict in the format: <key> -> <value>\\n

    Parameters
    ----------
    dict : dict
        Generic dictionary
    """    
    for k, v in dict.items():
        print(k, ' -> ', v)


def addInMatrix(matrix, taxon, level):
    """Adds the counting of a animal to dict matrix.

    Parameters
    ----------
    matrix : dict
        Each key is an Animal Name, and its value is a int representing how
        many times this animal appears. Like:
        {'RE2': 16, 'RE1': 1}
    taxon : list
        List with 2 or 1 animal. Like:
        ['RE1', 'RE7']
    level : int
        Which animal count adds to the matrix.
    """    
    try:
        matrix[taxon[level]] += 1
    except:
        matrix[taxon[level]] = 1


def replaceEscapeCode(word):
    """Replace a str escape code for a real escape code.

    Parameters
    ----------
    word : str
        Escape code to be verified.

    Returns
    -------
    _type_
        _description_
    """    
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