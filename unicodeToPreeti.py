unicodeToPreetiDict = \
    {
        "अ": "c",
        "आ": "cf",
        "ा": "f",
        "इ": "O",
        "ई": "O{",
        "र्": "{",
        "उ": "p",
        "ए": "P",
        "े": "]",
        "ै": "}",
        "ो": "f]",
        "ौ": "f}",
        "ओ": "df]",
        "औ": "df}",
        "ं": "+",
        "ँ": "F",
        "ि": "l",
        "ी": "L",
        "ु": "'",
        "ू": '"',
        "क": "s",
        "ख": "v",
        "ग": "u",
        "घ": "3",
        "ङ": "ª",
        "च": "r",
        "छ": "5",
        "ज": "h",
        "झ": "´",
        "ञ": "`",
        "ट": "6",
        "ठ": "7",
        "ड": "8",
        "ढ": "9",
        "ण": "0f",
        "त": "t",
        "थ": "y",
        "द": "b",
        "ध": "w",
        "न": "g",
        "प": "k",
        "फ": "km",
        "ब": "a",
        "भ": "e",
        "म": "d",
        "य": "o",
        "र": "/",
        "रू": "?",
        "ृ": "[",
        "ल": "n",
        "व": "j",
        "स": ";",
        "श": "z",
        "ष": "if",
        "ज्ञ": "1",
        "ह": "x",
        "१": "!",
        "२": "@",
        "३": "#",
        "४": "$",
        "५": "%",
        "६": "^",
        "७": "&",
        "८": "*",
        "९": "(",
        "०": ")",
        "।": ".",
        "्": "\\",
        "ऊ": "pm",
        "-": " "
    }

def normalizeUnicode(unicodetext):
    index=-1
    normalized=''
    while index+1<len(unicodetext):
        index+=1
        character=unicodetext[index]
        try:
            try:
                if character!='र': # for aadha akshars
                    if unicodetext[index+1]=='्' and unicodetext[index+2]!=' ' and unicodetext[index+2]!='।' and unicodetext[index+2]!=',':
                        if unicodetext[index+2]!='र': 
                            if unicodeToPreetiDict[character] in list('wertyuxasdghjkzvn'):
                                normalized+=chr(ord(unicodeToPreetiDict[character])-32)
                                index+=1
                                continue
                            elif character == 'स':
                                normalized+=':'
                                index+=1
                                continue
                            elif character== 'ष':
                                normalized+='i'
                                index+=1
                                continue
                if unicodetext[index-1]!='र' and character=='्' and unicodetext[index+1]=='र': # for kaagpaat
                    if unicodetext[index-1]!='ट' and unicodetext[index-1]!='ठ' and unicodetext[index-1]!='ड':
                        normalized+='|'
                        index+=1
                        continue
                    else:
                        normalized+='«'
                        index+=1
                        continue
            except IndexError:
                pass
            normalized+=character
        except KeyError:
            normalized+=character
    normalized=normalized.replace('त|','q') # for tra
    return normalized
        

inputfile="unicode.txt"
with open(inputfile,"r",encoding='utf-8') as fp:
    unicodetext=fp.read()
normalizedunicodetext=normalizeUnicode(unicodetext)
converted=''
index=-1
while index+1<len(normalizedunicodetext):
    index+=1
    character=normalizedunicodetext[index]
    if character=='\ufeff':
        continue
    try:
        try:
            if normalizedunicodetext[index+2]  == 'ि': # for constructs like त्ति
                if character in list('WERTYUXASDGHJK:ZVN'):
                    converted+='l'+character+unicodeToPreetiDict[normalizedunicodetext[index+1]]
                    index+=2
                    continue
            if normalizedunicodetext[index+3] == 'ि': # for the likes of ष्ट्रिय
                if normalizedunicodetext[index+2] == '|' or normalizedunicodetext[index+2] == '«':
                    if character in list('WERTYUXASDGHJK:ZVNIi'):
                        converted+='l'+character+unicodeToPreetiDict[normalizedunicodetext[index+1]]+normalizedunicodetext[index+2]
                        index+=3
                        continue
            if normalizedunicodetext[index+1]=='ि': # for normal hraswo ukaar
                converted+='l'+unicodeToPreetiDict[character]
                index+=1
                continue
            if normalizedunicodetext[index+1]=='्' and character=='र': # for reph as in वार्ता
                if normalizedunicodetext[index+3]=='ा' or normalizedunicodetext[index+3]=='ो' or normalizedunicodetext[index+3]=='ौ' or normalizedunicodetext[index+3]=='े' or normalizedunicodetext[index+3]=='ै' or normalizedunicodetext[index+3]=='ि' or normalizedunicodetext[index+3]=='ी':
                    converted+=unicodeToPreetiDict[normalizedunicodetext[index+2]]+unicodeToPreetiDict[normalizedunicodetext[index+3]]+'{'
                    index+=3
                    continue
                converted+=unicodeToPreetiDict[normalizedunicodetext[index+2]]+'{'
                index+=2
                continue
            
        except IndexError:
            pass
        converted+= unicodeToPreetiDict[character]
    except KeyError:
        converted+=character
    
    converted=converted.replace('Si','I') # Si in preeti is aadha ka aadha ष, so replace with I which is aadha क्ष
    converted=converted.replace('H`','1') # H` is the product of composite nature of unicode ज्ञ
    converted=converted.replace('b\w','4') # b\w means in preeti द halanta ध, so replace the composite
    converted=converted.replace('z|','>') # composite for श्र
    converted=converted.replace("/'",'?') # composite for रु
    converted=converted.replace('/"','¿') # composite for रू
    converted=converted.replace('Tt','Q') # composite for त्त
    converted=converted.replace('b\lj','lå') # composite for द्वि
    converted=converted.replace('b\j','å') # composite for द्व

with open('output.txt','w') as fp:
    fp.write(converted)