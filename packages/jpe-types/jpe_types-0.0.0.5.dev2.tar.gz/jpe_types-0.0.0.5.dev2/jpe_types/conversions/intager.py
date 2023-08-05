"conversions retaining to ints"

import json, os
data = json.load(open(f"{os.path.dirname(os.path.realpath(__file__))}/intConversions.json","r"))
"convig data from json"

def baseN(num,b,numerals=data["baseKeys"]): # from https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base writen by jellyfishtree
    """convert to sys with base b
    
    converts a number to a string representing that number base b
    @param num: the number to be converted
    @type num: int
    @param b: the baise of the system
    @type b: int
    
    @param numerals: optional the keyes representing the values
    @type numerals: string
    """
    assert isinstance(num ,(int)), f"num must be an int or a float not {type(num)}"
    assert isinstance(b, int), f"the base must be an int"
    assert isinstance(numerals, str),f"numerals must be string not {type(num)}"
    assert len(numerals) >= b, f"not enough numerals, the length of numerals sting dose not contain enogh characters to reprisent a system with base {b} since it hase {len(numerals)} keys"
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def convertTointFrombaseStr(num, b, numerals=data["baseKeys"]):
    """convert a base str to int 

    @param num: the input to be converted
    @type num: string

    @param b: the base of the sys to convert from
    @type b: int

    @param numerals: optional the keyes representing the values
    @type numerals: string
    """
    assert isinstance(num ,str), f"num must be an int or a float not {type(num)}"
    assert isinstance(b, int), f"the base must be an int"
    assert isinstance(numerals, str),f"numerals must be string not {type(num)}"
    assert len(numerals) >= b, f"not enough numerals, the length of numerals sting dose not contain enogh characters to reprisent a system with base {b} since it hase {len(numerals)} keys"

    res = 0
    for idx, key in enumerate(num):
        res += b**(len(num) - idx-1)*(numerals.index(key))
    return res
