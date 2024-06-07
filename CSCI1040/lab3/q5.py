
import re


MORSE_CODES = {
    'A':'.-'   , 'B':'-...'  , 'C':'-.-.'  , 'D':'-..'   , 'E':'.'     ,
    'F':'..-.' , 'G':'--.'   , 'H':'....'  , 'I':'..'    , 'J':'.---'  , 
    'K':'-.-'  , 'L':'.-..'  , 'M':'--'    , 'N':'-.'    , 'O':'---'   , 
    'P':'.--.' , 'Q':'--.-'  , 'R':'.-.'   , 'S':'...'   , 'T':'-'     ,
    'U':'..-'  , 'V':'...-'  , 'W':'.--'   , 'X':'-..-'  , 'Y':'-.--'  , 
    'Z':'--..' , ',':'--..--', '.':'.-.-.-', '?':'..--..', '-':'-....-',
    '1':'.----', '2':'..---' , '3':'...--' , '4':'....-' , '5':'.....' , 
    '6':'-....', '7':'--...' , '8':'---..' , '9':'----.' , '0':'-----'
}

class MorseTranslator:
    def encode(self, text):
        self.text=list(text.upper())
        temp=[]
        for i in self.text:
            temp.append(MORSE_CODES.get(i, i))
        
        temp = ' '.join(temp)

        return str(temp)

    def decode(self, code):  
        self.code = code.split()
        temp=[]
        for i in self.code:
            temp.append(list(MORSE_CODES.keys())[list(MORSE_CODES.values()).index(i)])

        temp = ''.join(temp)
        return temp
       

translator = MorseTranslator()

mesg = "HI, WHAT NEWS TODAY?"
code = translator.encode(mesg)
print(code)

mesg = "UKRAINE CRISIS, FEB 22"
code = translator.encode(mesg)
print(code)

code = ".--. .-. .- -.--  ..-. --- .-.  ..- -.- .-. .- .. -. .. .- -. ... .-.-.-"
decoded = translator.decode(code)
print(decoded)

code = ".- .-. .  -.-- --- ..-  ... - .- -.-- .. -. --.  - ..- -. . -.. ..--.."
decoded = translator.decode(code)
print(decoded)
